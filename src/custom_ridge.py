import numpy as np
from functools import partial

def prever(x_i, beta):
    return np.dot(x_i, beta)

def calcular_erro(x_i, y_i, beta):
    return y_i - prever(x_i, beta)

def gradiente_erro_quadratico(x_i, y_i, beta):
    # Calcula o gradiente do Erro Quadrático Médio (MSE).
    return -2 * calcular_erro(x_i, y_i, beta) * x_i

def penalidade_ridge(beta, alpha):
    # Calcula a penalidade L2 (Ridge).
    return alpha * np.dot(beta[1:], beta[1:])

def gradiente_penalidade_ridge(beta, alpha):
    #Calcula o gradiente da penalidade L2, ignorando o intercepto (beta[0]).
    return np.concatenate(([0], 2 * alpha * beta[1:]))

def gradiente_custo_total_ridge(x_i, y_i, beta, alpha):
    # Soma o gradiente do erro com o gradiente da penalidade.
    grad_erro = gradiente_erro_quadratico(x_i, y_i, beta)
    grad_penalidade = gradiente_penalidade_ridge(beta, alpha)
    return np.add(grad_erro, grad_penalidade)

def descida_gradiente_estocastica(fn_gradiente, x, y, theta_inicial, taxa_aprendizado=0.001, epocas=200):
    # Otimizador SGD (Stochastic Gradient Descent). Minimiza a função de custo iterando sobre amostras aleatórias.
    theta = np.array(theta_inicial)
    indices = np.arange(len(y))
    np.random.seed(42) 
    
    for _ in range(epocas):
        np.random.shuffle(indices)
        for i in indices:
            gradiente = fn_gradiente(x[i], y[i], theta)
            theta = theta - taxa_aprendizado * gradiente
            
    return theta

def treinar_ridge_numpy(X_matriz, y_vetor, alpha, taxa_aprendizado=0.001, epocas=200):
    # Recebe a matriz de features, o vetor alvo e o hiperparâmetro alpha.
    np.random.seed(42)
    beta_inicial = np.random.rand(X_matriz.shape[1])
    
    fn_grad_parcial = partial(gradiente_custo_total_ridge, alpha=alpha)
    
    return descida_gradiente_estocastica(
        fn_grad_parcial, 
        X_matriz, 
        y_vetor, 
        beta_inicial, 
        taxa_aprendizado, 
        epocas
    )