from model import BertTextModel_encode_layer
from transformers import BertTokenizer
import torch
from config import parsers
import time
import os

class Pred_question:
    def __init__(self):
        pass

    def pred_main(self):
        # start = time.time()
        args = parsers()
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        #选择保存的最佳模型
        root, name = os.path.split(args.save_model_best)
        save_best = os.path.join(root, str(args.select_model_last) + "_" +name) #False_best_model.ph
        model = self.load_model(save_best, device, args)

        # print("模型预测结果：")
        self.pred_one(args, model, device)  # 预测一条文本


    def load_model(self,model_path, device, args):
        model = BertTextModel_encode_layer().to(device)
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model


    def text_class_name(self,texts, pred, args):
        results = torch.argmax(pred, dim=1)
        results = results.cpu().numpy().tolist()
        classification = open(args.classification, "r", encoding="utf-8").read().split("\n")
        classification_dict = dict(zip(range(len(classification)), classification))
        return classification_dict[results[0]]


    def pred_one(self,text):
        args = parsers()
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        root, name = os.path.split(args.save_model_best)
        save_best = os.path.join(root, str(args.select_model_last) + "_" +name)
        model = self.load_model(save_best, device, args)

        tokenizer = BertTokenizer.from_pretrained(parsers().bert_pred)

        encoded_pair = tokenizer(text, padding='max_length', truncation=True,  max_length=args.max_len, return_tensors='pt')
        token_ids = encoded_pair['input_ids']
        attn_masks = encoded_pair['attention_mask']
        token_type_ids = encoded_pair['token_type_ids']

        all_con = tuple(p.to(device) for p in [token_ids, attn_masks, token_type_ids])
        #放入预训练的模型进行训练
        pred = model(all_con)
        
        #获得结果
        results = torch.argmax(pred, dim=1)
        results = results.cpu().numpy().tolist()
        classification = open(args.classification, "r", encoding="utf-8").read().split("\n")
        classification_dict = dict(zip(range(len(classification)), classification))
        res=classification_dict[results[0]]
        
        # print(res)
        return res

if __name__=='__main__':
    a=Pred_question()
    while 1:
        text=input("问题: ")
        res=a.pred_one(text)
        print("Pred Class:  "+res)

    
        
