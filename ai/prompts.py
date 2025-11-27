"""Prompts estruturados para a IA de precificação"""

SYSTEM_PROMPT = """Você é o PricePro AI Assistant, um especialista sênior em precificação, estratégia comercial e finanças empresariais.

Sua função é ajudar pequenos e médios empreendedores a encontrarem o melhor preço possível para seus produtos, considerando:
- Todos os custos envolvidos (produção, impostos, taxas, despesas)
- Margem de lucro desejada
- Estratégia de mercado
- Competitividade
- Sustentabilidade do negócio

Diretrizes:
1. Sempre responda de forma clara, prática e orientada ao negócio
2. Justifique todas as recomendações com dados concretos
3. Considere o contexto e objetivos do empreendedor
4. Identifique riscos e oportunidades
5. Sugira ações práticas e implementáveis
6. Use linguagem acessível, evitando jargões técnicos quando possível

Formato de resposta: JSON estruturado conforme solicitado.
"""

def get_analysis_prompt(product_data: dict, user_goal: str, desired_margin: float) -> str:
    """Gera o prompt para análise de precificação"""
    
    product_name = product_data.get('name', 'Produto')
    category = product_data.get('category', 'Não especificada')
    production_cost = product_data.get('production_cost', 0)
    fixed_expenses = product_data.get('fixed_expenses', 0)
    variable_expenses = product_data.get('variable_expenses', 0)
    taxes = product_data.get('taxes', 0)
    marketplace_fee = product_data.get('marketplace_fee', 0)
    payment_fee = product_data.get('payment_fee', 0)
    shipping_fee = product_data.get('shipping_fee', 0)
    advertising_fee = product_data.get('advertising_fee', 0)
    
    total_cost = (
        production_cost + fixed_expenses + variable_expenses + 
        taxes + marketplace_fee + payment_fee + shipping_fee + advertising_fee
    )
    
    prompt = f"""Analise o seguinte produto e forneça recomendações de precificação:

**DADOS DO PRODUTO:**
- Nome: {product_name}
- Categoria: {category}

**ESTRUTURA DE CUSTOS:**
- Custo de Produção: R$ {production_cost:.2f}
- Despesas Fixas: R$ {fixed_expenses:.2f}
- Despesas Variáveis: R$ {variable_expenses:.2f}
- Impostos: R$ {taxes:.2f}
- Taxa de Marketplace: R$ {marketplace_fee:.2f}
- Taxa de Pagamento: R$ {payment_fee:.2f}
- Frete: R$ {shipping_fee:.2f}
- Publicidade: R$ {advertising_fee:.2f}
**CUSTO TOTAL: R$ {total_cost:.2f}**

**OBJETIVO DO EMPREENDEDOR:**
{user_goal}

**MARGEM DESEJADA:**
{desired_margin}%

**TAREFA:**
Forneça uma análise completa de precificação em formato JSON com a seguinte estrutura EXATA:

{{
  "preco_recomendado": <número com 2 casas decimais>,
  "margem_recomendada": <número com 2 casas decimais>,
  "preco_minimo": <número com 2 casas decimais>,
  "preco_premium": <número com 2 casas decimais>,
  "insights": [
    "Insight 1: Descrição detalhada do primeiro insight",
    "Insight 2: Descrição detalhada do segundo insight",
    "Insight 3: Descrição detalhada do terceiro insight"
  ],
  "riscos": [
    "Risco 1: Descrição detalhada do primeiro risco",
    "Risco 2: Descrição detalhada do segundo risco"
  ],
  "oportunidades": [
    "Oportunidade 1: Descrição detalhada da primeira oportunidade",
    "Oportunidade 2: Descrição detalhada da segunda oportunidade"
  ],
  "estrategia_sugerida": "Descrição completa da estratégia comercial recomendada (mínimo 3 frases)",
  "resumo_executivo": "Resumo executivo da análise (mínimo 4 frases, máximo 6 frases)",
  "pontos_sensibilidade": [
    {{"preco": <número>, "lucro": <número>, "margem": <número>}},
    {{"preco": <número>, "lucro": <número>, "margem": <número>}},
    {{"preco": <número>, "lucro": <número>, "margem": <número>}},
    {{"preco": <número>, "lucro": <número>, "margem": <número>}},
    {{"preco": <número>, "lucro": <número>, "margem": <número>}}
  ]
}}

**INSTRUÇÕES IMPORTANTES:**
1. Calcule o preço_recomendado considerando o custo total e a margem desejada
2. O preço_minimo deve cobrir todos os custos com margem mínima de segurança (5-10%)
3. O preço_premium deve ser 20-30% acima do preço recomendado para posicionamento premium
4. A margem_recomendada deve ser realista para o segmento e objetivo do empreendedor
5. Forneça pelo menos 3 insights práticos e acionáveis
6. Identifique pelo menos 2 riscos concretos
7. Sugira pelo menos 2 oportunidades de melhoria
8. A estratégia sugerida deve ser específica para este produto e objetivo
9. O resumo executivo deve sintetizar a análise de forma clara e objetiva
10. Os pontos_sensibilidade devem mostrar 5 cenários de preço diferentes (do mínimo ao premium) com lucro e margem calculados

**RESPONDA APENAS COM O JSON PURO, SEM FORMATAÇÃO MARKDOWN, SEM BLOCOS DE CÓDIGO, SEM EXPLICAÇÕES ADICIONAIS.**
"""
    
    return prompt
