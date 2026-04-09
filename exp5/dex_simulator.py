"""
DEX核心机制仿真模板
任务：实现AMM核心函数 + 无常损失计算
"""
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

class SimpleAMM:
    def __init__(self, reserve_x: float, reserve_y: float, fee: float = 0.003):
        """
        初始化流动性池
        :param reserve_x: 代币X储备量（如ETH）
        :param reserve_y: 代币Y储备量（如USDC）
        :param fee: 交易手续费率（默认0.3%）
        """
        self.reserve_x = reserve_x
        self.reserve_y = reserve_y
        self.fee = fee
        self.k = reserve_x * reserve_y  # 恒定乘积
    
    # ==================== 任务1：实现swap函数 ====================
    def swap_x_for_y(self, dx: float) -> float:
        """
        用dx数量的X代币兑换Y代币
        公式: (x + dx*(1-fee)) * (y - dy) = k
        TODO: 计算并返回实际获得的dy，更新储备金
        """
        # === 在此实现 ===
        # 1. 计算扣除手续费后的实际输入: dx_with_fee = 
        # 2. 根据恒定乘积公式计算dy: dy = 
        # 3. 更新储备金: self.reserve_x 和 self.reserver_y
        # 4. 返回dy
        pass
    
    # ==================== 任务2：实现无常损失计算 ====================
    @staticmethod
    def calculate_impermanent_loss(price_ratio_initial: float, price_ratio_final: float) -> float:
        """
        计算无常损失（IL）
        公式: IL = 2*sqrt(r) / (1+r) - 1, 其中r = price_final / price_initial
        TODO: 返回无常损失百分比（-0.05表示损失5%）
        """
        pass
    
    def add_liquidity(self, dx: float, dy: float) -> Tuple[float, float]:
        """添加流动性（简化版，按比例注入）"""
        total_value = self.reserve_x + self.reserve_y
        share_x = dx / (dx + self.reserve_x)
        share_y = dy / (dy + self.reserve_y)
        self.reserve_x += dx
        self.reserve_y += dy
        self.k = self.reserve_x * self.reserve_y
        return (dx, dy)

# ==================== 可视化滑点曲线 ====================
def plot_slippage_curve(amm: SimpleAMM, max_dx: float = 5.0):
    dx_list = np.linspace(0.1, max_dx, 50)
    dy_list = []
    for dx in dx_list:
        # 临时复制池状态避免污染
        temp_amm = SimpleAMM(amm.reserve_x, amm.reserve_y, amm.fee)
        dy = temp_amm.swap_x_for_y(dx)
        dy_list.append(dy)
    
    # 计算理论无滑点值（按初始价格）
    initial_price = amm.reserve_y / amm.reserve_x
    theoretical_dy = [dx * initial_price for dx in dx_list]
    
    plt.figure(figsize=(8, 5))
    plt.plot(dx_list, dy_list, label='reality (with slippage)')
    plt.plot(dx_list, theoretical_dy, '--', label='theory (without slippage)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('DEX slippage')
    plt.legend()
    plt.grid(True)
    plt.show()

# ==================== 主程序 ====================
if __name__ == "__main__":
    # 初始化50 ETH : 100,000 USDC的流动性池
    amm = SimpleAMM(reserve_x=50.0, reserve_y=100000.0)
    
    print("=== 测试swap功能 ===")
    dy = amm.swap_x_for_y(5.0)
    print(f"用5 ETH兑换获得 {dy:.2f} USDC")
    print(f"当前池状态: {amm.reserve_x:.2f} ETH, {amm.reserve_y:.2f} USDC")
    
    print("\n=== 计算无常损失 ===")
    il = SimpleAMM.calculate_impermanent_loss(
        price_ratio_initial=2000,  # 1 ETH = 2000 USDC
        price_ratio_final=3000     # 1 ETH = 3000 USDC
    )
    print(f"价格从2000涨至3000时，无常损失: {il*100:.2f}%")
    
    print("\n=== 生成滑点曲线 ===")
    plot_slippage_curve(amm)