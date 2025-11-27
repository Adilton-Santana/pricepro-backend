"""Engine de IA para análise de precificação usando Abacus.AI LLM APIs"""
import os
import json
import httpx
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AIEngine:
    """Engine de IA para análise de precificação"""
    
    def __init__(self):
        self.api_key = os.getenv("ABACUSAI_API_KEY")
        self.api_url = "https://apps.abacus.ai/v1/chat/completions"
        self.model = "gpt-4.1-mini"
        self.timeout = 60.0
        
        if not self.api_key:
            raise ValueError("ABACUSAI_API_KEY não configurada")
    
    async def analyze_pricing(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        """Analisa precificação usando a IA
        
        Args:
            prompt: Prompt do usuário com dados do produto
            system_prompt: Prompt de sistema com contexto da IA
        
        Returns:
            Dict com análise completa de precificação
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2500,
                "response_format": {"type": "json_object"}
            }
            
            logger.info(f"Enviando requisição para LLM API: {self.model}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    logger.error(f"Erro na API: {response.status_code} - {response.text}")
                    raise Exception(f"Erro na API de IA: {response.status_code}")
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Parse do JSON retornado
                analysis = json.loads(content)
                
                logger.info("Análise de precificação gerada com sucesso")
                return analysis
                
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear resposta JSON: {e}")
            raise Exception("Erro ao processar resposta da IA")
        except httpx.TimeoutException:
            logger.error("Timeout na requisição para LLM API")
            raise Exception("Timeout na análise de IA. Tente novamente.")
        except Exception as e:
            logger.error(f"Erro na análise de IA: {str(e)}")
            raise
    
    async def generate_quick_insights(self, product_data: Dict[str, Any]) -> list:
        """Gera insights rápidos sobre um produto
        
        Args:
            product_data: Dados do produto
        
        Returns:
            Lista de insights
        """
        try:
            prompt = f"""Com base nos seguintes dados de produto:

Nome: {product_data.get('name', 'Produto')}
Custo Total: R$ {product_data.get('total_cost', 0):.2f}
Preço Atual: R$ {product_data.get('ideal_price', 0):.2f}
Margem: {product_data.get('margin', 0):.1f}%

Forneça 3 insights rápidos e práticos em formato JSON:

{{
  "insights": [
    "Insight 1",
    "Insight 2",
    "Insight 3"
  ]
}}

Responda apenas com JSON puro, sem formatação.
"""
            
            result = await self.analyze_pricing(prompt, "Você é um especialista em precificação. Seja objetivo e prático.")
            return result.get("insights", [])
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights rápidos: {str(e)}")
            return []
