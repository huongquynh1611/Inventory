import sys 
website = "https://best.aliexpress.com/?lan=en"
from crawl_aliexpress import GetHomePage,GetProductList

def main(args):
    # param: cate subcate rate pricemin pricemax ....
    # empty -> null
    # này phải quy định rõ ràng theo thứ tự các thông số, 
    # nếu thông số nào ko có hoặc rỗng thì phải có kí tự/chuổi để ký hiệu rỗng
    print(args)

    cate = args[0]
    # subcate = args[1]
    # rate = args[2]

    print("cate = ", cate)
    
    dict_cate = GetHomePage(website)
    cate_url = dict_cate[cate]  
    data = GetProductList(cate_url,max_num_pages=1)   

    file = open("data.json", "w")
    file.write(data)   

 
if __name__ == "__main__":
    main(sys.argv[1:])
    