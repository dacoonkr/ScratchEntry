import BLL.bll as BLL

def stats(bll: BLL.BLLfile):
    tablehead = "========「" + bll._name + "」의 통계 ========"
    print(tablehead)
    print("스프라이트 개수: ", len(bll._objs))
    print("데이터 소스 개수: ", len(bll._global_srcs))
    print("자료 개수: ", len(bll._vars) + len(bll._casts))
    print("블럭 개수: ", bll._stat_block_cnt)
    print("=" * len(tablehead.encode("cp949")))