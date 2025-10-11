const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

// 🔑 SUA CHAVE API DO MERCADO PAGO AQUI
const MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-1662920071781236-101001-234f1cb2b9b56e8e70dbb602fcf271bb-1853327613'; // ← SUBSTITUA POR SUA CHAVE REAL

app.use(express.json());
app.use(express.static('public'));

// Habilita CORS
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

// Rota para criar pagamento Pix REAL
app.post('/create-pix-payment', async (req, res) => {
    try {
        const { amount } = req.body;
        
        console.log('Criando pagamento Pix na API Mercado Pago...');
        
        // Requisição REAL para a API do Mercado Pago
        const response = await axios.post('https://api.mercadopago.com/v1/orders', {
            "type": "online",
            "total_amount": amount.toFixed(2),
            "external_reference": "ext_ref_" + Date.now(),
            "processing_mode": "automatic",
            "transactions": {
                "payments": [
                    {
                        "amount": amount.toFixed(2),
                        "payment_method": {
                            "id": "pix",
                            "type": "bank_transfer"
                        },
                        "expiration_time": "P1D" // 1 dia de expiração
                    }
                ]
            },
            "payer": {
                "email": "cliente@exemplo.com"
            }
        }, {
            headers: {
                'Authorization': `Bearer ${MERCADOPAGO_ACCESS_TOKEN}`,
                'Content-Type': 'application/json',
                'X-Idempotency-Key': 'key_' + Date.now()
            }
        });

        console.log('✅ Pagamento criado com sucesso:', response.data.id);
        res.json(response.data);
        
    } catch (error) {
        console.error('❌ Erro na API Mercado Pago:', error.response?.data || error.message);
        res.status(500).json({ 
            error: 'Erro ao criar pagamento',
            details: error.response?.data 
        });
    }
});

// Rota para verificar status REAL
app.get('/payment-status/:paymentId', async (req, res) => {
    try {
        const response = await axios.get(
            `https://api.mercadopago.com/v1/payments/${req.params.paymentId}`,
            {
                headers: {
                    'Authorization': `Bearer ${MERCADOPAGO_ACCESS_TOKEN}`
                }
            }
        );
        res.json(response.data);
    } catch (error) {
        console.error('Erro ao verificar status:', error.response?.data);
        res.status(500).json({ error: 'Erro ao verificar pagamento' });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Servidor rodando na porta ${PORT}`);
    console.log(`🌐 Acesse: http://localhost:${PORT}`);
});