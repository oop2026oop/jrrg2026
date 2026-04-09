import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

# ================= 1. 实验配置 =================
@dataclass
class LabConfig:
    initial_price: float = 2000.0      # ETH 初始价格 (USDC)
    initial_capital: float = 10000.0   # 初始本金 (USDC)
    fee_rate: float = 0.003            # 0.3% 费率
    price_range: tuple = (1800.0, 2200.0)  # V3 集中区间 [P_min, P_max]
    days: int = 100                    # 模拟周期
    daily_volume: float = 5000000.0  # 日均交易量 (USDC)
    market_mode: str = "oscillating"   # "oscillating"(震荡) 或 "trending"(单边)

config = LabConfig()

# ================= 2. 价格路径生成器 =================
def generate_price_path(cfg: LabConfig) -> np.ndarray:
    """生成价格路径：默认震荡，可设置单边趋势"""
    np.random.seed(42)
    if cfg.market_mode == "oscillating":
        returns = np.random.normal(0.0, 0.015, cfg.days)  # 均值0，高波动
    else:
        returns = np.random.normal(0.008, 0.012, cfg.days) # 均值正，单边上涨
    prices = cfg.initial_price * np.exp(np.cumsum(returns))
    return np.insert(prices, 0, cfg.initial_price)

# ================= 3. V3 集中流动性池 =================
class UniswapV3ConcentratedPool:
    def __init__(self, cfg: LabConfig):
        self.P0 = cfg.initial_price
        self.capital = cfg.initial_capital
        self.fee_rate = cfg.fee_rate
        self.P_min, self.P_max = cfg.price_range
        
        self.L = 0.0          # 流动性深度
        self.fees_earned = 0.0
        self.current_price = self.P0
        
        self._init_liquidity()
        
        # 历史记录
        self.value_history = []
        self.fees_history = []
        self.il_history = []
        self.in_range_history = []

    def _init_liquidity(self):
        """
        TODO 1: 根据初始资本和价格区间计算流动性 L
        数学提示:
          在初始价格 P0 处:
          x = L * (1/√P0 - 1/√P_max)
          y = L * (√P0 - √P_min)
          资本约束: capital = x * P0 + y
          代入化简可得 L 的显式公式。请实现计算并赋值给 self.L
        """
        pass

    def _get_reserves(self, P: float) -> tuple[float, float]:
        """
        TODO 2: 根据当前价格 P 计算资产持仓 (x: ETH数量, y: USDC数量)
        分段逻辑:
          1. P < P_min   : 价格低于区间，全部转为 USDC
          2. P_min ≤ P ≤ P_max : 区间内，按 V3 标准公式计算
          3. P > P_max   : 价格高于区间，全部转为 ETH
        """
        pass

    def step(self, new_price: float, trade_volume: float) -> float:
        """单步模拟：更新价格 -> 计算仓位 -> 累积手续费 -> 计算 IL"""
        self.current_price = new_price
        x, y = self._get_reserves(new_price)

        # TODO 3: 计算当前底层资产市值（不含手续费）
        portfolio_value = ... 

        # TODO 4: 判断是否在区间内，若在区间内则按交易量收取手续费
        # 简化模型：日内价格视为稳定，若在 [P_min, P_max] 内则赚取全额手续费
        in_range = self.P_min <= new_price <= self.P_max
        if in_range:
            self.fees_earned += ...

        total_value = portfolio_value + self.fees_earned

        # TODO 5: 计算相对于 HODL 策略的无常损失 (IL)
        # HODL 策略：初始本金一半买 ETH，一半留 USDC，长期持有不动
        # HODL 价值 = (capital/2) + (capital/(2*P0)) * new_price
        # IL = (total_value / hodl_value) - 1
        hodl_value = ...
        il = ...

        # 记录历史数据
        self.value_history.append(total_value)
        self.fees_history.append(self.fees_earned)
        self.il_history.append(il)
        self.in_range_history.append(in_range)

        return total_value

# ================= 4. 仿真运行与可视化 =================
def run_simulation(cfg: LabConfig):
    prices = generate_price_path(cfg)
    pool = UniswapV3ConcentratedPool(cfg)
    
    for i in range(len(prices)-1):
        pool.step(prices[i+1], cfg.daily_volume)
        
    days = np.arange(len(prices))
    hodl_values = (cfg.initial_capital / 2) * (1 + prices / cfg.initial_price)
    
    p_min, p_max = cfg.price_range
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # 图1: 资产价值 vs HODL
    axes[0].plot(days, hodl_values, label="HODL Strategy", color="gray", linestyle="--", linewidth=2)
    axes[0].plot(days, pool.value_history, label="V3 Concentrated LP", color="#2563eb", linewidth=2)
    axes[0].set_ylabel("Portfolio Value (USDC)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 图2: 累积手续费 vs 无常损失
    ax1 = axes[1]
    ax1.plot(days, pool.fees_history, label="Accrued Fees", color="#16a34a", linewidth=2)
    ax1.set_ylabel("Fees (USDC)", color="#16a34a")
    ax1.tick_params(axis='y', labelcolor="#16a34a")
    
    ax2 = ax1.twinx()
    ax2.plot(days, pool.il_history, label="Impermanent Loss", color="#dc2626", linewidth=2)
    ax2.set_ylabel("Impermanent Loss (%)", color="#dc2626")
    ax2.tick_params(axis='y', labelcolor="#dc2626")
    axes[1].legend(loc="upper left")
    axes[1].grid(True, alpha=0.3)
    
    # 图3: 价格路径与区间状态
    axes[2].plot(days, prices, label="ETH Price", color="black", linewidth=2)
    axes[2].axhline(p_min, color="#f59e0b", linestyle=":", linewidth=2, label=f"P_min={p_min}")
    axes[2].axhline(p_max, color="#f59e0b", linestyle=":", linewidth=2, label=f"P_max={p_max}")
    axes[2].fill_between(days, p_min, p_max, where=pool.in_range_history, color="#3b82f6", alpha=0.15)
    axes[2].set_ylabel("Price (USDC)")
    axes[2].set_xlabel("Simulation Days")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.suptitle(f"Uniswap V3 Concentrated Liquidity Simulation | Mode: {cfg.market_mode.upper()}", fontsize=14, y=0.98)
    plt.tight_layout()
    plt.show()
    

# ================= 5. 执行实验 =================
if __name__ == "__main__":
    # 切换 market_mode 观察不同现象
    # config.market_mode = "oscillating"  # 优点体现：震荡市
    config.market_mode = "trending"      # 缺点体现：单边趋势市
    run_simulation(config)