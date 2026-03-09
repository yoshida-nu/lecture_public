def run_program(memory):
    register = 0
    pc = 0  # プログラムカウンタ
    print(f"メモリ内の命令: {memory}")
    print(f"レジスタの初期状態: {register}")
    while pc < len(memory):
        op, value = memory[pc]
        print(f"===={pc+1}回目のサイクル====")
        print(f"プログラムカウンタ: {pc}")
        print(f"命令: {op}")
        print(f"データ: {value}")

        if op == "LOAD":
            register = value
        elif op == "ADD":
            register += value
        elif op == "SUB":
            register -= value
        elif op == "JUMP":
            pc = value
            continue
        
        print(f"現在のレジスタ: {register}")
        
        pc += 1
    
    print(f"====== 実行完了 ======")
    print("最終結果:", register)

    