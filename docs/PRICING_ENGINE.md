# 📐 Motor de Precificação - Documentação Técnica

## 👁️ Visão Geral

O Motor de Precificação é o core do PricePro. Ele calcula preços de venda baseado em uma série de variáveis e custos, garantindo que o empreendedor cubra todos os gastos e atinja suas margens desejadas.

## 🎯 Objetivo

Calcular **3 preços distintos** para cada produto:

1. **Preço Mínimo**: O menor preço possível que cobre todos os custos (margem = 0)
2. **Preço Ideal**: Preço que inclui a margem de lucro desejada pelo empreendedor
3. **Preço Premium**: Preço ideal multiplicado por um fator (preparado para otimização via IA)

## 🧩 Componentes de Custo

### 1. Custos Variáveis (por unidade)

```python
custo_variavel_total = (
    cost_price +           # Custo de produção/compra
    variable_costs +       # Despesas variáveis
    additional_fees        # Taxas adicionais
)
```

**Exemplos:**
- `cost_price`: Matéria-prima, custo de fornecedor
- `variable_costs`: Embalagem, etiqueta, sacola
- `additional_fees`: Taxa de maquininha, frete por unidade

### 2. Despesas Fixas (rateadas)

```python
fixed_costs_allocated  # Despesas fixas divididas entre produtos
```

**Exemplos:**
- Aluguel do local
- Salários fixos
- Contas (luz, água, internet)
- Marketing fixo

**Importante:** Despesas fixas são usadas apenas no cálculo de break-even, não entram diretamente no preço.

### 3. Impostos

```python
tax_percentage  # Percentual de impostos sobre o preço de venda
```

**Exemplos:**
- Simples Nacional: ~6-15%
- Lucro Presumido: ~13-32%
- ICMS, ISS, PIS, COFINS

### 4. Taxas de Canal

```python
sales_channels = [
    {"channel": "Loja Física", "fee_percentage": 0},
    {"channel": "Marketplace", "fee_percentage": 15},
    {"channel": "E-commerce Próprio", "fee_percentage": 5}
]
```

**Exemplos:**
- Mercado Livre: 12-16%
- Magazine Luiza: 18-22%
- iFood (restaurantes): 12-27%
- Instagram Shopping: 5%

## 📊 Fórmulas de Cálculo

### 1️⃣ Preço Mínimo

Cobre **apenas** os custos variáveis e impostos. Margem de lucro = 0.

```python
preco_minimo = custo_variavel_total / (1 - (impostos / 100))
```

**Exemplo:**
- Custo variável total: R$ 50
- Impostos: 15%

```python
preco_minimo = 50 / (1 - 0.15) = 50 / 0.85 = R$ 58,82
```

**Validação:**
- Receita: R$ 58,82
- Impostos (15%): R$ 8,82
- Custo: R$ 50,00
- **Lucro: R$ 0**

---

### 2️⃣ Preço Ideal

Inclui a **margem de lucro desejada** pelo empreendedor.

```python
preco_ideal = custo_variavel_total / (1 - (impostos / 100) - (margem / 100))
```

**Exemplo:**
- Custo variável total: R$ 50
- Impostos: 15%
- Margem desejada: 30%

```python
preco_ideal = 50 / (1 - 0.15 - 0.30) = 50 / 0.55 = R$ 90,91
```

**Validação:**
- Receita: R$ 90,91
- Impostos (15%): R$ 13,64
- Custo: R$ 50,00
- **Lucro: R$ 27,27 (30% da receita)**

---

### 3️⃣ Preço Premium

Preço ideal multiplicado por um **fator premium** (ex: 1.3 = +30%).

```python
preco_premium = preco_ideal * fator_premium
```

**Exemplo:**
- Preço ideal: R$ 90,91
- Fator premium: 1.3 (+30%)

```python
preco_premium = 90.91 * 1.3 = R$ 118,18
```

**Uso futuro com IA:**
O fator premium pode ser ajustado dinamicamente por IA considerando:
- Demanda do mercado
- Preços da concorrência
- Sazonalidade
- Elasticidade de preço

---

## 📊 Cálculo por Canal de Venda

Quando o produto é vendido em canais com taxas (ex: marketplaces), o preço deve ser ajustado:

```python
preco_no_canal = preco_base / (1 - (taxa_canal / 100))
```

**Exemplo:**
- Preço ideal: R$ 90,91
- Taxa do Mercado Livre: 15%

```python
preco_no_mercado_livre = 90.91 / (1 - 0.15) = 90.91 / 0.85 = R$ 106,95
```

**Validação:**
- Receita bruta: R$ 106,95
- Taxa do canal (15%): R$ 16,04
- **Receita líquida: R$ 90,91** (igual ao preço ideal)

---

## ⚠️ Break-Even (Ponto de Equilíbrio)

Número de unidades que precisam ser vendidas para **cobrir as despesas fixas**.

```python
break_even = despesas_fixas / lucro_por_unidade
```

**Exemplo:**
- Despesas fixas: R$ 1.000
- Lucro por unidade (preço ideal): R$ 27,27

```python
break_even = 1000 / 27.27 = 36,67 unidades
```

**Interpretação:**
Vendendo 37 unidades no preço ideal, você cobre todas as despesas fixas.

---

## 📦 Exemplo Completo

### Entrada

```json
{
  "cost_price": 50.00,
  "tax_percentage": 15.0,
  "variable_costs": 5.00,
  "fixed_costs_allocated": 1000.00,
  "sales_channels": [
    {"channel": "Loja Física", "fee_percentage": 0},
    {"channel": "Marketplace", "fee_percentage": 15}
  ],
  "additional_fees": 3.00,
  "desired_margin_percentage": 30.0,
  "premium_factor": 1.3
}
```

### Cálculos

1. **Custo Variável Total:**
   ```
   50 + 5 + 3 = R$ 58,00
   ```

2. **Preço Mínimo:**
   ```
   58 / (1 - 0.15) = R$ 68,24
   Lucro: R$ 0
   ```

3. **Preço Ideal:**
   ```
   58 / (1 - 0.15 - 0.30) = R$ 105,45
   Lucro: R$ 31,64
   ```

4. **Preço Premium:**
   ```
   105.45 * 1.3 = R$ 137,09
   Lucro: R$ 57,82
   ```

5. **Break-Even:**
   ```
   1000 / 31.64 = 31,62 unidades
   ```

6. **Preços por Canal:**
   
   **Loja Física (taxa 0%):**
   - Mínimo: R$ 68,24
   - Ideal: R$ 105,45
   - Premium: R$ 137,09
   
   **Marketplace (taxa 15%):**
   - Mínimo: R$ 80,28 (= 68.24 / 0.85)
   - Ideal: R$ 124,06 (= 105.45 / 0.85)
   - Premium: R$ 161,28 (= 137.09 / 0.85)

---

## 🔧 Implementação

O motor está implementado em `services/price_calculation_service.py`:

```python
class PriceCalculationService:
    @staticmethod
    def _calculate_prices(
        cost_price: float,
        tax_percentage: float,
        variable_costs: float,
        fixed_costs_allocated: float,
        sales_channels: List[SalesChannel],
        additional_fees: float,
        desired_margin_percentage: float,
        premium_factor: float
    ) -> PriceCalculationResult:
        # ... implementação ...
```

### Uso via API

**Simulação:**
```bash
POST /simulation/calculate
```

**Produto existente:**
```bash
POST /products/{id}/calculate-price?premium_factor=1.3
```

---

## 💡 Dicas para Empreendedores

### 1. Determine sua margem

Margens típicas por setor:
- **Alimentos**: 10-30%
- **Vestuário**: 40-60%
- **Eletrônicos**: 8-15%
- **Cosméticos**: 50-80%
- **Artesanato**: 50-100%

### 2. Considere todos os custos

Não esqueça:
- ✅ Embalagem
- ✅ Etiquetas
- ✅ Frete
- ✅ Sacolas
- ✅ Taxa de maquininha
- ✅ Tempo de produção (seu trabalho tem valor!)

### 3. Ajuste por canal

Se você vende em múltiplos canais, calcule o preço para cada um considerando suas taxas específicas.

### 4. Use o break-even

Saiba quantas unidades precisa vender para cobrir seus custos fixos mensais.

---

## 🚀 Próximas Evoluções

- [ ] Integração com IA para sugerir fator premium ideal
- [ ] Análise de preços da concorrência
- [ ] Recomendação de margem por categoria
- [ ] Alertas de preço muito baixo/alto
- [ ] Simulação de cenários ("e se...")
- [ ] Gráficos de lucro por volume
- [ ] Comparação entre produtos

---

**🎯 Documente seu conhecimento e precifique com inteligência!**
