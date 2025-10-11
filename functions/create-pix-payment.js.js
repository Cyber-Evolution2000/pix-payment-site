const mercadopago = require('mercadopago');

// Configura o Mercado Pago
mercadopago.configure({
    access_token: process.env.MERCADOPAGO_ACCESS_TOKEN
});

exports.handler = async function(event, context) {
    // Só permite POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Método não permitido' })
        };
    }

    try {
        const { amount } = JSON.parse(event.body);

        // Cria o pagamento no Mercado Pago
        const paymentData = {
            transaction_amount: amount,
            description: 'Pagamento via Pix',
            payment_method_id: 'pix',
            payer: {
                email: 'cliente@email.com',
                first_name: 'Cliente',
                last_name: 'Silva',
                identification: {
                    type: 'CPF',
                    number: '12345678909'
                }
            },
            notification_url: 'https://webhook.site/your-webhook', // Opcional
            additional_info: {
                items: [
                    {
                        id: '1',
                        title: 'Produto Teste',
                        description: 'Descrição do produto',
                        quantity: 1,
                        unit_price: amount,
                        category_id: 'others'
                    }
                ]
            }
        };

        const payment = await mercadopago.payment.create(paymentData);

        return {
            statusCode: 200,
            body: JSON.stringify(payment.body)
        };

    } catch (error) {
        console.error('Erro:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ 
                error: 'Erro ao criar pagamento',
                details: error.message 
            })
        };
    }
};