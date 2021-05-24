import torch
from sentence_transformers import SentenceTransformer, models, util
from db import db_instance, add_embedding_column
from posts_orm import PostsOrm, posts_get_all, add_post


model_name = 'paraphrase-xlm-r-multilingual-v1'


class SBert:

    model = None
    gpu = False

    def __init__(self):
        if torch.cuda.is_available():
            self.model = SentenceTransformer(model_name, device='cuda')
            self.gpu = True
        else:
            self.model = SentenceTransformer(model_name)

        add_embedding_column('users', 'embedding')
        add_embedding_column('groups', 'embedding')
        add_embedding_column('posts', 'embedding')


