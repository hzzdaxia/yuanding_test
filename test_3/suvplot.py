import csv
import matplotlib.pyplot as plt

class SuvPlot:
    Models = []
    MonthlySales = []
    AnnualSales = []

    def loadFile(self):
        # 加载销量数据的文件
        return csv.reader(open('suv.csv','r',encoding='utf-8'));

    def loadData(self):
        # 加载提取数据
        first = True
        file = self.loadFile()
        for suv in file:
            if(first):
                first = False
                continue
            self.Models.append(suv[1])
            self.MonthlySales.append(int(suv[2]))
            self.AnnualSales.append(int(suv[3]))

    def plot(self):
        # 解决中文乱码
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False

        plt.bar(self.Models, self.MonthlySales, label="月销量")
        plt.gcf().set_size_inches(16,8)
        plt.savefig("月销量.png")

        # 清空当前数据
        plt.clf()

        plt.bar(self.Models, self.AnnualSales, label="年销量")
        plt.gcf().set_size_inches(16,8)
        plt.savefig("年销量.png")

        # 清空当前数据
        plt.clf()

        plt.pie(self.MonthlySales,labels=self.Models,
                autopct='%1.1f%%')
        plt.title('月销量比例')
        plt.gcf().set_size_inches(8,8)
        plt.savefig("月销量比例.png")
        plt.clf()

        plt.pie(self.AnnualSales,labels=self.Models,
                autopct='%1.1f%%')
        plt.title('年销量比例')
        plt.gcf().set_size_inches(8,8)
        plt.savefig("年销量比例.png")
        plt.clf()


sp = SuvPlot()
sp.loadData()
sp.plot()




