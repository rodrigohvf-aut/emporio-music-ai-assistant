# Sample conversations

These examples use the local SQLite database and the store policy retrieval layer.

## Product availability

Customer: Quais violões estão disponíveis por até R$ 1.000?

Assistant: Encontrei os produtos disponíveis que correspondem à busca e ao limite informado, com preço e estoque consultados na base operacional.

## Store policy

Customer: Posso devolver um produto?

Assistant: Você pode solicitar uma devolução online em até 7 dias corridos após o recebimento, conforme as condições da loja.

## Price and stock lookup

Customer: Quanto custa o Yamaha C40?

Assistant: Yamaha C40 Nylon Natural custa R$ 599.90 e tem 12 unidade(s) em estoque.

## Non-trivial order lookup

Customer: Qual é o status do pedido 1?

Assistant: O pedido 1 está com status 'entregue'. Código de rastreio: BRAB1234567BR. Previsão de entrega: 2025-10-25.

## Out-of-scope request

Customer: Qual é a previsão do tempo hoje?

Assistant: Posso ajudar apenas com produtos, preços, estoque, promoções, pedidos e políticas da Empório da Música.

## Policy and promotion rules

Customer: Qual é o desconto no PIX? Posso combinar com uma promoção?

Assistant: O pagamento via PIX tem 5% de desconto, sem acumular com outras promoções.
