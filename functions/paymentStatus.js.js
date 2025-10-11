const mercadopago = require('mercadopago');

mercadopago.configure({
    access_token: process.env.MERCADOPAGO_ACCESS_TOKEN
});

exports.handler = async function(event, context) {
    // Só permite GET
    if (event.httpMethod !== 'GET') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Método não permitido' })
        };
    }

    try {
        const { id } = event.queryStringParameters;

        if (!id) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'ID do pagamento não fornecido' })
            };
        }

        // Busca o pagamento no Mercado Pago
        const payment = await mercadopago.payment.get(id);

        return {
            statusCode: 200,
            body: JSON.stringify({ 
                status: payment.body.status,
                id: payment.body.id
            })
        };

    } catch (error) {
        console.error('Erro:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ 
                error: 'Erro ao verificar pagamento',
                details: error.message 
            })
        };
    }
};