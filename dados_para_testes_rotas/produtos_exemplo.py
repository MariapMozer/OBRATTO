"""
Produtos fictícios de exemplo para demonstração
Imagens são URLs públicas do Unsplash e Pexels
"""

PRODUTOS_EXEMPLO = [
    {
        "nome": "Fone de Ouvido Wireless Premium",
        "descricao": "Fone de ouvido com cancelamento de ruído ativo, bateria de 40 horas e som de alta qualidade.",
        "preco": 299.99,
        "quantidade": 15,
        "foto": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=400&fit=crop"
    },
    {
        "nome": "Teclado Mecânico RGB",
        "descricao": "Teclado mecânico para jogos com switches customizáveis e iluminação RGB programável.",
        "preco": 450.00,
        "quantidade": 8,
        "foto": "https://images.unsplash.com/photo-1587829191301-32f21c82d1d7?w=500&h=400&fit=crop"
    },
    {
        "nome": "Mouse Gamer Profissional",
        "descricao": "Mouse com sensor 16000 DPI, 8 botões programáveis e design ergonômico.",
        "preco": 199.90,
        "quantidade": 22,
        "foto": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=400&fit=crop"
    },
    {
        "nome": "Monitor 4K 27 polegadas",
        "descricao": "Monitor ultralarga 4K com HDR, 144Hz e suporte para NVIDIA G-Sync.",
        "preco": 1899.00,
        "quantidade": 5,
        "foto": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&h=400&fit=crop"
    },
    {
        "nome": "Webcam 1080p Full HD",
        "descricao": "Webcam com foco automático, microfone integrado e visão de 90 graus.",
        "preco": 249.99,
        "quantidade": 12,
        "foto": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&h=400&fit=crop"
    },
    {
        "nome": "Mousepad Grande XL",
        "descricao": "Mousepad resistente à água com base antiderrapante. Perfeito para jogadores.",
        "preco": 89.90,
        "quantidade": 45,
        "foto": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=400&fit=crop"
    },
    {
        "nome": "Headset Gamer 7.1 Surround",
        "descricao": "Headset com som surround 7.1, microfone de cancelamento de ruído e almofadas confortáveis.",
        "preco": 349.99,
        "quantidade": 10,
        "foto": "https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=500&h=400&fit=crop"
    },
    {
        "nome": "Suporte Ajustável para Monitor",
        "descricao": "Suporte de mesa com inclinação ajustável para monitores até 27 polegadas.",
        "preco": 129.90,
        "quantidade": 30,
        "foto": "https://images.unsplash.com/photo-1545887917-3e24b2f5d5eb?w=500&h=400&fit=crop"
    },
    {
        "nome": "Cabo HDMI 2.1 8K",
        "descricao": "Cabo HDMI 2.1 com suporte a 8K 120Hz e conector dourado de alta durabilidade.",
        "preco": 79.99,
        "quantidade": 60,
        "foto": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=400&fit=crop"
    },
    {
        "nome": "Carregador Rápido 65W USB-C",
        "descricao": "Carregador rápido universal com múltiplas portas USB-C e proteção inteligente.",
        "preco": 169.90,
        "quantidade": 35,
        "foto": "https://images.unsplash.com/photo-1618765896829-f5c8e3d17a13?w=500&h=400&fit=crop"
    },
    {
        "nome": "Hub USB 7 Portas com Fonte",
        "descricao": "Hub USB 3.0 com 7 portas, carregamento rápido e alimentação dedicada.",
        "preco": 149.99,
        "quantidade": 18,
        "foto": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500&h=400&fit=crop"
    },
    {
        "nome": "Cooler para Notebook 17 polegadas",
        "descricao": "Base refrigeradora com 5 ventiladores silenciosos para dissipação de calor.",
        "preco": 199.90,
        "quantidade": 14,
        "foto": "https://images.unsplash.com/photo-1588872657840-790ff3bde172?w=500&h=400&fit=crop"
    }
]

"""
URLs de imagens alternativas (caso as principais falhem):
- Eletrônicos genéricos: https://images.pexels.com/
- Produtos tech: https://images.unsplash.com/
- Icons: https://www.flaticon.com/

Atributos importantes para cada produto:
- nome: String (max 200 caracteres)
- descricao: String (max 500 caracteres)
- preco: Float (com 2 casas decimais)
- quantidade: Integer (quantidade em estoque)
- foto: URL da imagem (suporta HTTP/HTTPS)
"""
