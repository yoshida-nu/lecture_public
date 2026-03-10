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

def choose_time_unit(seconds):
    """
    秒で与えられた時間を，見やすい単位に変換して返す
    """
    time_units = [
        ("秒", 1),
        ("ミリ秒", 10**-3),
        ("マイクロ秒", 10**-6),
        ("ナノ秒", 10**-9),
        ("ピコ秒", 10**-12),
        ("フェムト秒", 10**-15),
    ]

    for unit_name, unit_value in time_units:
        converted = seconds / unit_value
        if 1 <= converted < 1000:
            return converted, unit_name

    return seconds, "秒"


def frequency_to_hz(value, aux=""):
    """
    周波数の値と接頭語から Hz に変換する
    例: 3.2, 'G' -> 3.2e9
    """
    prefix = {
        "": 1,
        "K": 10**3,
        "M": 10**6,
        "G": 10**9,
    }

    if aux not in prefix:
        raise ValueError("aux は '', 'K', 'M', 'G' のいずれかにしてください")

    if value <= 0:
        raise ValueError("周波数は 0 より大きい値にしてください")

    return value * prefix[aux]


def clock_to_period(value, aux=""):
    """
    クロック周波数から 1クロック当たりの時間を求める
    戻り値:
        period_sec : 秒
        display_value, display_unit : 表示用
    """
    frequency_hz = frequency_to_hz(value, aux)
    period_sec = 1 / frequency_hz
    display_value, display_unit = choose_time_unit(period_sec)
    return period_sec, display_value, display_unit


def instruction_time(value, aux, cpi):
    """
    クロック周波数と CPI から 1命令当たりの実行時間を求める
    戻り値:
        inst_sec : 秒
        display_value, display_unit : 表示用
    """
    if cpi <= 0:
        raise ValueError("CPI は 0 より大きい値にしてください")

    period_sec, _, _ = clock_to_period(value, aux)
    inst_sec = period_sec * cpi
    display_value, display_unit = choose_time_unit(inst_sec)
    return inst_sec, display_value, display_unit


def instruction_time_to_mips(inst_sec):
    """
    1命令当たりの実行時間（秒）から MIPS を求める
    MIPS = 1秒間に何百万命令実行できるか
    """
    if inst_sec <= 0:
        raise ValueError("1命令当たりの実行時間は 0 より大きい必要があります")

    return 1 / (inst_sec * 10**6)


def cpu_performance_report(value, aux, cpi):
    """
    CPU性能をまとめて表示する授業用レポート関数
    """
    frequency_hz = frequency_to_hz(value, aux)

    period_sec, period_value, period_unit = clock_to_period(value, aux)
    inst_sec, inst_value, inst_unit = instruction_time(value, aux, cpi)
    mips_value = instruction_time_to_mips(inst_sec)

    print("=" * 40)
    print("【CPUの性能評価】")
    print(f"クロック周波数: {value}{aux}Hz")
    print(f"Hzで表すと: {frequency_hz:g} Hz")
    print()
    print(f"1クロック当たりの時間: {period_value:g}{period_unit}")
    print(f"1命令当たりの実行時間: {inst_value:g}{inst_unit} （{cpi} CPI）")
    print(f"MIPS: {mips_value:g} M回／秒")
    print("=" * 40)
    print()
