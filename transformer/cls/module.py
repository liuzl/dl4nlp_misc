import torch 
import torch.nn as nn 
import torch.nn.functional as F 
from torch.nn import Parameter 
from torch import einsum 
from torch import rand

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 


class SelfAttention(nn.Module): 

    def __init__(self, n_head, d_embed, use_einsum):
        super(SelfAttention, self).__init__() 
        self.h = n_head 
        self.use_einsum = use_einsum
        factor = 2 / (d_embed) ** 0.5 # for initialization of weights
         
        # mapping matrices to transform input vectors to query, key, and value vectors 
        self.wq = Parameter(factor * (rand(d_embed, n_head * d_embed) - 1))
        self.wk = Parameter(factor * (rand(d_embed, n_head * d_embed) - 1)) 
        self.wv = Parameter(factor * (rand(d_embed, n_head * d_embed) - 1)) 

        # weights and biases for a feedforward layer 
        self.wf = Parameter(factor * (rand(n_head * d_embed, d_embed) - 1))
        self.bf = Parameter(factor * (rand(d_embed) - 1))

        # total number of trainable parameters
        self.num_params = torch.numel(self.wq) + torch.numel(self.wk) + \
                          torch.numel(self.wv) + torch.numel(self.wf) + \
                          torch.numel(self.bf)

    def forward(self, x):
        B, T, D = x.size() # batch size, time (sequence) length, embedding dimension
        H = self.h # number of heads 

        # query, key, and value from input vectors
        # [B, T, D] * [D, H*D] -> [B, T, H*D]
        if self.use_einsum:
            q = einsum('bij,jk->bik', [x, self.wq])
            k = einsum('bij,jk->bik', [x, self.wk])
            v = einsum('bij,jk->bik', [x, self.wv])
        else:
            q = x.matmul(self.wq) 
            k = x.matmul(self.wk) 
            v = x.matmul(self.wv) 
        
        # re-arranging q, k, and v for independent head-wise computation 
        # [B, T, H*D] -> [B, T, H, D] -> [B, H, T, D]
        q = q.reshape(B, T, H, D).transpose(1, 2) 
        k = k.reshape(B, T, H, D).transpose(1, 2)
        v = v.reshape(B, T, H, D).transpose(1, 2) 

        # weights from q and k 
        # [B, H, T, D] * [B, H, D, T] -> [B, H, T, T]
        if self.use_einsum:
            w = einsum('bijk,bilk->bijl', [q, k]) / (D ** 0.5)
        else:
            w = q.matmul(k.transpose(2, 3)) / (D ** 0.5)

        w = F.softmax(w, dim=3) 

        # output
        if self.use_einsum:
            # [B, H, T, T] * [B, H, T, D] -> [B, H, T, D]
            y = einsum('bijk,bikl->bijl', [w, v])
        else: 
            y = w.matmul(v) 

        # [B, H, T, D] => [B, T, H, D] -> [B, T, H*D] 
        y = y.transpose(1, 2).reshape(B, T, H*D)

        if self.use_einsum:
            # [B, T, H*D] * [H*D, D] -> [B, T, D] 
            y = einsum('bij,jk->bik', [y, self.wf]) + self.bf
        else:
            y = y.matmul(self.wf) + self.bf 

        return y 

    def count_parameters(self):
        total_params = 0
        for param in self.state_dict():
            dim_params = self.state_dict()[param].size()
            total_params += dim_params.numel()
            print(param, dim_params)
        print('Total number of parameters:', total_params)


class TransformerBlock(nn.Module):

    def __init__(self, n_head, d_embed, use_einsum):
        super(TransformerBlock, self).__init__()
        self.attention = SelfAttention(n_head, d_embed, use_einsum) 
        self.norm1 = nn.LayerNorm(d_embed) 
        self.norm2 = nn.LayerNorm(d_embed) 
        self.linear1 = nn.Linear(d_embed, d_embed) 
        self.linear2 = nn.Linear(d_embed, d_embed)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        x = self.norm1(x + self.attention(x)) 
        x = self.norm2(x + self.linear2(F.relu(self.linear1(x)))) 
        return self.dropout(x) 


class EmbeddingBlock(nn.Module):

    def __init__(self, d_embed, n_token, n_sequence, embedding_pos): 
        super(EmbeddingBlock, self).__init__() 
        self.token_embedding = nn.Embedding(n_token, d_embed)
        self.embedding_pos = embedding_pos
        if embedding_pos:
            self.position_embedding = nn.Embedding(n_sequence, d_embed) 
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        token_embeds = self.token_embedding(x)

        if self.embedding_pos:
            b, t, d = token_embeds.size() 
            pos_embeds = self.position_embedding(
                torch.arange(t, device=device))[None, :, :].expand(b, t, d) 
            return self.dropout(token_embeds + pos_embeds) 
        else:
            return self.dropout(token_embeds) 


class ClassificationTransformer(nn.Module):

    def __init__(self, n_layer, n_head, d_embed, n_token, n_sequence, 
                 n_class, embedding_pos):
        super(ClassificationTransformer, self).__init__() 
        
        self.embedding = EmbeddingBlock(d_embed, n_token, n_sequence, embedding_pos)
        
        transformer_layers = []
        for _ in range(n_layer):
            transformer_layers.append(
                TransformerBlock(n_head, d_embed, use_einsum=True))
        self.transformer_layers = nn.Sequential(*transformer_layers) 

        self.linear = nn.Linear(d_embed, n_class) 
        
    def forward(self, x):
        x = self.embedding(x) 
        x = self.transformer_layers(x) 
        x = x.mean(dim=1)
        x = self.linear(x) 
        return F.log_softmax(x, dim=1) 


