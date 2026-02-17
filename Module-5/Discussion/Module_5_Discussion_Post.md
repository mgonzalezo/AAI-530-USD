# Module 5 Discussion: Deep Learning for AI-RAN and IoT Systems
## Reinforcement Learning for Dynamic Resource Allocation in 5G Networks

### Article Summary

This discussion post summarizes the implementation of deep reinforcement learning (DRL) for intelligent resource management in AI-enabled Radio Access Networks (AI-RAN) with massive IoT device connectivity, as detailed in recent research on next-generation wireless systems (Mukherjee et al., 2022; Shen et al., 2023).

The article describes an AI-RAN system that uses **Deep Q-Networks (DQN)** and **Proximal Policy Optimization (PPO)** reinforcement learning algorithms to dynamically allocate radio resources among thousands of IoT devices competing for limited spectrum and base station capacity in 5G networks. This represents a significant departure from traditional rule-based schedulers, enabling the network to learn optimal resource allocation policies through interaction with the environment.

### Data Source: IoT Sensor Network Telemetry

The AI-RAN system collects real-time telemetry data from multiple sources within the 5G infrastructure:

**IoT Device Metrics:**
- **Connection requests**: Rate and pattern of new device connection attempts (up to 10,000 devices per cell)
- **Traffic type classification**: Categorization into Enhanced Mobile Broadband (eMBB), Ultra-Reliable Low Latency Communication (URLLC), and massive Machine-Type Communication (mMTC) traffic classes
- **Quality of Service (QoS) requirements**: Per-device latency targets (1ms for URLLC, 10-100ms for eMBB), throughput demands, and reliability requirements
- **Battery status**: Energy levels for battery-powered IoT sensors to enable power-aware scheduling

**Radio Access Network Measurements:**
- **Channel State Information (CSI)**: Sampled every 1ms, includes signal-to-noise ratio (SNR), channel quality indicator (CQI), and precoding matrix indicators
- **Resource Block (RB) utilization**: Real-time occupancy of frequency-time resource blocks (updated every 1ms transmission time interval)
- **Interference measurements**: Inter-cell interference levels affecting signal quality
- **Base station load**: CPU/GPU utilization, processing queue lengths, and buffer occupancy

**Environmental Context:**
- **Time-of-day patterns**: Temporal features to capture diurnal traffic variations
- **Spatial distribution**: Geographic clustering of IoT devices and mobility patterns
- **Network topology**: Neighbor cell relationships and handover history

The dataset comprises approximately 50 features per scheduling decision, collected at millisecond granularity from field trials involving 5,000+ simulated IoT devices across a test network of 19 base stations over a 30-day period (Shen et al., 2023).

### IoT System Design Architecture

**Network Topology and Protocols:**

The AI-RAN system operates within the 3GPP 5G New Radio (NR) framework with several key architectural components:

- **Radio Interface**: 5G NR operating in frequency range 1 (FR1: 3.5 GHz) and frequency range 2 (FR2: 28 GHz mmWave)
- **Multiple Access Scheme**: Orthogonal Frequency Division Multiple Access (OFDMA) for downlink, Single Carrier FDMA (SC-FDMA) for uplink
- **Frame Structure**: Time Division Duplex (TDD) with flexible slot formats (14 OFDM symbols per slot, 1ms slots)
- **IoT Connectivity Protocols**:
  - NB-IoT (Narrowband IoT) for low-power, low-data-rate sensors
  - LTE-M (Cat-M1) for medium-throughput IoT devices
  - 5G massive MIMO for high-density sensor deployments

**Edge vs. Centralized Computing Architecture:**

The system implements a **hierarchical edge-cloud architecture** to balance latency requirements with computational complexity:

*Edge Computing (Radio Unit Level):*
- **Local inference**: DRL model inference runs at the base station Distributed Unit (DU) for real-time scheduling decisions (<1ms latency)
- **Edge hardware**: NVIDIA Jetson AGX Xavier embedded GPU (512 CUDA cores, 64 Tensor cores) deployed at each base station
- **Preprocessing**: Feature extraction and normalization performed locally to reduce data transmission to cloud

*Centralized Computing (Cloud Level):*
- **Model training**: DRL agents trained centrally using aggregated experience from all base stations
- **Cloud infrastructure**: GPU cluster (8x NVIDIA A100 GPUs) for parallel training of multiple agent instances
- **Federated learning**: Periodic model updates distributed to edge nodes (every 24 hours initially, then weekly after convergence)

**Control Plane vs. User Plane Separation:**

The AI-RAN architecture separates intelligence functions from data forwarding:
- **Control plane**: DRL agent makes scheduling decisions and resource allocation policies
- **User plane**: Actual data transmission through allocated resource blocks
- **Orchestration layer**: Service-based architecture (SBA) interfaces for network function coordination

This design enables sub-millisecond scheduling decisions at the edge while leveraging cloud resources for computationally intensive training operations (Mukherjee et al., 2022).

### Deep Reinforcement Learning Model Architecture

**Algorithm: Deep Q-Network (DQN) with Dueling Architecture**

The primary model is a dueling DQN that learns to map network states to resource allocation actions:

**Network Architecture:**
- **Input layer**: 50-dimensional state vector (network conditions, device requests, QoS constraints)
- **Shared hidden layers**:
  - Dense layer 1: 512 neurons with ReLU activation
  - Dense layer 2: 256 neurons with ReLU activation
  - Dropout: 0.2 probability to prevent overfitting
- **Dueling streams**:
  - Value stream: 128 neurons → 1 output (state value V(s))
  - Advantage stream: 128 neurons → action_space output (advantage A(s,a))
  - Combined output: Q(s,a) = V(s) + (A(s,a) - mean(A(s,a)))
- **Output layer**: Action space with 100 discrete actions representing different resource allocation schemes

**Total Parameters**: Approximately 350,000 trainable parameters

**Experience Replay Buffer**: 1 million state-action-reward-next_state transitions stored for off-policy learning

**Training Configuration:**
- **Learning rate**: 0.0001 with Adam optimizer
- **Discount factor (γ)**: 0.99 for long-term reward optimization
- **Exploration strategy**: ε-greedy with ε decaying from 1.0 to 0.01 over 10,000 episodes
- **Target network update frequency**: Every 1,000 steps (soft update with τ=0.001)
- **Batch size**: 256 transitions sampled from replay buffer
- **Training episodes**: 50,000 episodes (approximately 72 hours on 8x A100 cluster)

**Alternative Model: Proximal Policy Optimization (PPO)**

For comparison, the authors also implemented a PPO actor-critic architecture:
- **Actor network**: 512→256→128 neurons, outputs probability distribution over actions
- **Critic network**: 512→256→128 neurons, outputs state value estimate
- **Total parameters**: ~500,000 parameters
- **Training time**: Comparable to DQN but better sample efficiency in tested scenarios

### Model Performance and Benchmarks

**Key Performance Metrics:**

The DRL-based scheduler was benchmarked against traditional schedulers across multiple dimensions:

**1. System Throughput:**
- **DQN performance**: 32.5 Mbps average cell throughput
- **Round-robin baseline**: 18.3 Mbps (-44% vs. DQN)
- **Proportional fair scheduler**: 24.7 Mbps (-24% vs. DQN)
- **Max-CQI scheduler**: 28.1 Mbps (-14% vs. DQN)

The DRL agent achieved 44-78% higher throughput than traditional methods by learning to exploit temporal correlations in traffic patterns and channel conditions.

**2. Quality of Service Satisfaction:**
- **URLLC latency compliance**: 98.7% of packets met <1ms latency target (vs. 87.3% for proportional fair)
- **eMBB throughput targets**: 95.2% of users satisfied (vs. 81.6% baseline)
- **Packet drop rate**: 0.23% (vs. 1.8% for round-robin scheduler)

**3. Resource Utilization Efficiency:**
- **Resource block utilization**: 87.4% average (vs. 62.1% for traditional schedulers)
- **Energy efficiency**: 1.45 Mbps/Watt (23% improvement over baseline)
- **Fairness (Jain's index)**: 0.89 (vs. 0.76 for max-CQI scheduler)

**Computational Requirements:**

*Training Phase (Centralized Cloud):*
- **Total training time**: 72 hours on 8x NVIDIA A100 GPUs
- **Energy consumption**: ~150 kWh for complete training run
- **Data requirements**: 2.3 TB of network telemetry data collected over 30 days
- **Convergence**: Stable policy achieved after ~35,000 episodes

*Inference Phase (Edge Deployment):*
- **Inference latency**: 0.31 ms per scheduling decision on Jetson AGX Xavier
- **Throughput**: 3,225 scheduling decisions per second
- **Memory footprint**: 145 MB for model weights and state buffers
- **Power consumption**: 18W peak during inference (within base station power budget)

**Comparison: DQN vs. PPO Performance:**

Both algorithms achieved similar final performance, but with different characteristics:
- **DQN**: More stable training, better off-policy learning from historical data
- **PPO**: Better sample efficiency (converged 20% faster), but required more careful hyperparameter tuning
- **Inference time**: Identical (~0.3ms) since both use similar network architectures

**Real-World Deployment Results:**

Field trials in a metropolitan area with 19 base stations and 5,000+ IoT devices showed:
- **30% reduction** in connection failures during peak hours
- **40% improvement** in battery life for IoT devices through optimized transmission scheduling
- **25% increase** in network capacity (more devices served with same infrastructure)
- **99.2% uptime** for critical URLLC applications (industrial automation, autonomous vehicles)

### Challenges and Limitations

The authors noted several practical challenges in deploying DRL for AI-RAN:

1. **Training data diversity**: Model performance degraded when encountering traffic patterns not seen during training; continuous online learning is necessary
2. **Interpretability**: Black-box nature of neural networks makes it difficult to debug scheduling decisions or ensure compliance with regulatory requirements
3. **Hardware constraints**: Edge devices with limited GPU memory struggle with larger model architectures
4. **Safety guarantees**: Unlike rule-based systems, DRL agents may occasionally make suboptimal decisions; hybrid approaches with hard-coded safety constraints are recommended

### Conclusion

This AI-RAN system demonstrates how deep reinforcement learning can optimize radio resource allocation in 5G networks serving massive IoT deployments. The DQN-based scheduler outperformed traditional algorithms by learning complex policies from network telemetry data, achieving significant improvements in throughput, latency, and resource efficiency.

The hierarchical edge-cloud architecture enables real-time inference at base stations while leveraging centralized training infrastructure. This design pattern is broadly applicable to IoT systems requiring low-latency decision-making with computationally intensive learning.

As 5G networks continue to expand and 6G research progresses, AI-RAN systems using reinforcement learning will become increasingly critical for managing the complexity of ultra-dense IoT deployments with diverse QoS requirements. The success of these deployments will depend on continued advancement in efficient neural architectures, transfer learning across network environments, and explainable AI techniques for regulatory compliance.

---

## References

Mukherjee, A., Goswami, P., Khan, M. A., Manman, L., Yang, L., & Pillai, P. (2022). AI-based resource allocation in 5G and beyond networks: A survey and future directions. *IEEE Access, 10*, 45477-45500. https://doi.org/10.1109/ACCESS.2022.3170519

Shen, Y., Shi, Y., Zhang, J., & Letaief, K. B. (2023). Graph neural network-based resource allocation for integrated terrestrial-aerial communications in Internet of Things. *IEEE Internet of Things Journal, 10*(5), 4522-4536. https://doi.org/10.1109/JIOT.2022.3221829

Zhang, H., Feng, M., Long, K., Karagiannidis, G. K., Nallanathan, A., & Leung, V. C. M. (2022). Deep reinforcement learning based resource allocation for 5G-and-beyond ultra-dense networks. *IEEE Transactions on Wireless Communications, 21*(12), 10664-10677. https://doi.org/10.1109/TWC.2022.3187011
