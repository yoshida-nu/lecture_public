def transmission_efficiency(transmission_speed, line_speed):
    """
    transmission_speed : 実際の伝送速度 (Mbps)
    line_speed : 回線速度 (Mbps)
    """
    # 伝送効率 = (伝送速度 ÷ 回線速度) × 100
    efficiency = transmission_speed / line_speed * 100

    print(f'伝送効率（小数点以下2桁まで）: {efficiency:.2f} [%]')

def transmission_time(line_speed, efficiency, data_size):
    """
    line_speed : 回線速度 (Mbps)
    efficiency : 伝送効率 (%)
    data_size  : データ量 (MB)
    """

    # 伝送速度 = (伝送効率 ÷ 100) × 回線速度
    transmission_speed = (efficiency / 100) * line_speed

    # 伝送時間 = データ量 ÷ 伝送速度
    # ただし MB → Mbit に変換するため ×8
    transmission_time = (data_size * 8) / transmission_speed
    
    print(f'伝送速度（小数点以下2桁まで）: {transmission_speed:.2f} [Mbps]')
    print(f'伝送時間（小数点以下2桁まで）: {transmission_time:.2f} [秒]')

