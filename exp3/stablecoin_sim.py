# stablecoin_simulation
import numpy as np
import matplotlib.pyplot as plt

# ==================== 稳定币模拟类 ====================
class StablecoinSimulator:
    def __init__(self, initial_supply=1000000, arbitrage_efficiency=0.8):
        self.price = 1.00
        self.supply = initial_supply
        self.arbitrage_efficiency = arbitrage_efficiency
        self.confidence = 1.0  # 市场信心 (0-1)
        self.history = {
            'price': [],
            'supply': [],
            'confidence': []
        }
    
    def step(self, shock=0) -> None:
        """模拟一个时间步长（1天）"""
        # 1. 外部冲击
        self.confidence -= shock
        
        # 2. 恐慌抛售压力（信心越低，抛售越大）
        panic_pressure = (1 - self.confidence) * 0.05 + np.random.normal(0, 0.005)
        
        # 3. 套利修复机制（价格<1时触发）
        # TODO 实现套利修复逻辑: 
        # 当价格小于1时, 套利力量=价差*套利效率*市场信心; 否则套利力量为0
        # 销毁率应与套利力量成正比 (比例系数设为 0.1) burn_rate = ...
        # 新供应 = 旧供应 × (1 - 销毁率)
        
        # 4. 价格更新
        self.price = self.price - panic_pressure + arbitrage_force
        self.price = max(0.01, self.price)
        
        # 5. 信心反馈（价格影响信心）
        # 实现信心衰减逻辑（价格<0.95时加速衰减）
        if self.price < 0.95:
            self.confidence *= 0.85
        
        # 6. 记录历史
        # TODO 更新self.history
    
    def run_simulation(self, days=90, crisis_day=10, shock_magnitude=0.3):
        # TODO 运行完整模拟, 逻辑:循环调用step函数, 当到crisis_day的时候添加强度shock_magnitude
        
        return self.history

# ==================== 任务1：基础模拟 ====================
def run_basic_simulation():
    """运行基础模拟，观察价格恢复"""
    print("任务1：基础模拟...\n")
    
    sim = StablecoinSimulator()
    history = sim.run_simulation(days=90, crisis_day=10)
    
    return history

# ==================== 任务3：死亡螺旋重现 ====================
def death_spiral_simulation():
    """模拟UST式死亡螺旋"""
    print("死亡螺旋重现...\n")
    
    sim = StablecoinSimulator()
    history = sim.run_simulation(days=90, crisis_day=10, shock_magnitude=0.5)
    
    return history

# ==================== 可视化函数 ====================
def plot_simulation_results(*histories, labels):
    """绘制多组模拟结果对比"""
    plt.figure(figsize=(14, 5))
    
    # TODO 按要求完成函数
    '''
        可视化要求:
        1. 两张子图水平并列. 左图内容为稳定币价格受到冲击时普通情况和陷入死亡螺旋的情况, 右图内容为市场信心在受到冲击时普通情况和陷入死亡螺旋的情况.
        2. 左图标题为"Price stability simulation", 横坐标为"Days", 纵坐标为"Price(USD)"; 
            右图标题为"Market confidence changes", 横坐标为"Days", 纵坐标为"Market confidence"
        3. 两幅图的横轴范围均为0~90, 纵轴范围均为0~1
        4. 左图在Price=1.0处有一条水平虚线, 在Days=10处有一条竖直虚线.
        5. 左图有四个图例, 右图有3个图例.
        6. 两幅图都需要加网格背景.
    '''


# ==================== 主程序 ====================
def main():
    print("=" * 60)
    print("实验4：稳定币机制模拟与风险建模")
    print("=" * 60)
    print()
    
    # 任务1
    history1 = run_basic_simulation()
    
    # 任务2
    history2 = death_spiral_simulation()
    
    # 可视化对比
    plot_simulation_results(
        history1, history2,
        labels=['basis sim', 'death spiral']
    )

if __name__ == '__main__':
    main()