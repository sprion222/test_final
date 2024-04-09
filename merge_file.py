from filesplit.merge import Merge

class merge_all:
    def __init__(self) -> None:
        pass

    def merge_main(self):
        merge1=Merge(inputdir="./model/model_cut",outputdir="./model",outputfilename="False_best_model.pth")
        merge1.merge()

        merge2=Merge(inputdir="./bert-base-chinese/pytorch_model_cut",outputdir="./bert-base-chinese",outputfilename="pytorch_model.bin")
        merge2.merge()