const questoes = [
  {pergunta: "O que é um sistema operacional?", opcoes: ["Um programa que gerencia o hardware e softwares do computador", "Um antivírus", "Um programa de edição de texto", "Um navegador de internet"], correta: 0},
  {pergunta: "Qual atalho é usado para copiar um texto no Windows?", opcoes: ["Ctrl + V", "Ctrl + X", "Ctrl + C", "Ctrl + Z"], correta: 2},
  {pergunta: "O que significa a sigla CPU?", opcoes: ["Central Processing Unit", "Computer Personal Unit", "Control Processing User", "Central Power Unit"], correta: 0},
  {pergunta: "Qual destes é um navegador de internet?", opcoes: ["Excel", "Firefox", "Word", "PowerPoint"], correta: 1},
  {pergunta: "Qual a função principal do Excel?", opcoes: ["Edição de imagens", "Planilhas eletrônicas", "Criação de textos", "Navegar na internet"], correta: 1},
  {pergunta: "Qual extensão pertence a um arquivo do Word?", opcoes: [".xls", ".docx", ".ppt", ".jpg"], correta: 1},
  {pergunta: "O que é a internet?", opcoes: ["Um software de edição", "Uma rede mundial de computadores", "Um antivírus", "Um jogo online"], correta: 1},
  {pergunta: "O que é hardware?", opcoes: ["Programas de computador", "Parte física do computador", "Sistema operacional", "Aplicativos"], correta: 1},
  {pergunta: "Qual destes é um dispositivo de entrada?", opcoes: ["Monitor", "Teclado", "Impressora", "Caixa de som"], correta: 1},
  {pergunta: "O que é backup?", opcoes: ["Exclusão de arquivos", "Cópia de segurança de dados", "Instalação de programas", "Abertura de sites"], correta: 1},
  {pergunta: "O que é um antivírus?", opcoes: ["Software para proteger contra malwares", "Sistema operacional", "Planilha eletrônica", "Rede social"], correta: 0},
  {pergunta: "Qual a função do PowerPoint?", opcoes: ["Apresentações de slides", "Planilhas", "Navegação na web", "Edição de vídeos"], correta: 0},
  {pergunta: "O que é um PDF?", opcoes: ["Formato de imagem", "Formato de documento portátil", "Sistema de rede", "Extensão de áudio"], correta: 1},
  {pergunta: "Qual destes é um sistema operacional?", opcoes: ["Windows", "Chrome", "Firefox", "Excel"], correta: 0},
  {pergunta: "Qual tecla é usada para atualizar uma página no navegador?", opcoes: ["F2", "F5", "Ctrl+C", "Esc"], correta: 1},
  {pergunta: "Qual destes é um software de edição de imagens?", opcoes: ["Word", "Excel", "Photoshop", "Access"], correta: 2},
  {pergunta: "Qual a função do mouse?", opcoes: ["Armazenar dados", "Interagir com a interface gráfica", "Exibir imagens", "Executar programas"], correta: 1},
  {pergunta: "O que é nuvem (cloud)?", opcoes: ["Um antivírus", "Armazenamento de dados online", "Sistema de áudio", "Extensão de vídeo"], correta: 1},
  {pergunta: "Qual atalho salva um documento no Word?", opcoes: ["Ctrl+V", "Ctrl+S", "Ctrl+C", "Ctrl+X"], correta: 1},
  {pergunta: "Qual destes é um dispositivo de saída?", opcoes: ["Monitor", "Mouse", "Teclado", "Scanner"], correta: 0}
];

let nomeAluno = "";
let cpfAluno = "";

// Captura dados do aluno
document.getElementById("dadosForm").addEventListener("submit", function(e){
  e.preventDefault();
  nomeAluno = document.getElementById("nome").value.trim();
  cpfAluno = document.getElementById("cpf").value.trim();
  if(nomeAluno === "" || cpfAluno.length !== 11 || !/^\d{11}$/.test(cpfAluno)){
    Swal.fire("Atenção", "Preencha corretamente seu nome e CPF (11 dígitos).", "warning");
    return;
  }
  document.querySelector(".dados-aluno").classList.add("hidden");
  document.getElementById("prova").classList.remove("hidden");
  carregarQuestoes();
});

function carregarQuestoes(){
  const container = document.getElementById("questoes");
  container.innerHTML = "";
  questoes.forEach((q,i) => {
    const div = document.createElement("div");
    div.classList.add("questao");
    div.innerHTML = `<p><b>${i+1}. ${q.pergunta}</b></p>`;
    q.opcoes.forEach((op, j) => {
      div.innerHTML += `<label><input type="radio" name="q${i}" value="${j}"> ${op}</label><br>`;
    });
    container.appendChild(div);
  });
}

// Corrige prova
document.getElementById("quizForm").addEventListener("submit", function(e){
  e.preventDefault();
  let acertos = 0;
  questoes.forEach((q,i)=>{
    const resposta = document.querySelector(`input[name="q${i}"]:checked`);
    if(resposta && parseInt(resposta.value) === q.correta){
      acertos++;
    }
  });
  const total = questoes.length;
  const percentual = Math.round((acertos/total)*100);
  let msg = `Você acertou ${acertos} de ${total} questões. Aproveitamento: ${percentual}%.`;
  document.getElementById("mensagemResultado").textContent = msg;
  document.getElementById("resultado").classList.remove("hidden");
  if(percentual >= 50){
    document.getElementById("btnPagamento").classList.remove("hidden");
  }
});

// Botão "Gerar Certificado" redireciona para checkout Mercado Pago
document.getElementById("btnPagamento").addEventListener("click", async function(){
  const payload = {
    amount: 19.90,
    order_id: "cert_" + Date.now(),
    payer_email: "teste@example.com",
    payer_name: nomeAluno,
    payer_cpf: cpfAluno,
    course: "Informática Básica"
  };

  try {
    const response = await fetch("https://toward-dept-monday-subtle.trycloudflare.com/create_preference.php", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if(data.success && data.init_point){
      Swal.fire({
        title: 'Pagamento',
        text: 'Você será redirecionado para o pagamento via Mercado Pago.',
        icon: 'info',
        confirmButtonText: 'Ir para pagamento'
      }).then(()=>{
        window.location.href = data.init_point;
      });
    } else {
      Swal.fire("Erro","Falha ao criar pagamento.","error");
      console.log(data);
    }
  } catch (err) {
    Swal.fire("Erro","Falha ao conectar com o servidor.","error");
    console.error(err);
  }
});

// Gera PDF certificado
function gerarCertificado(){
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF();
  pdf.setFontSize(16);
  pdf.text("CERTIFICADO DE CONCLUSÃO", 60, 30);
  pdf.setFontSize(12);
  pdf.text(`Certificamos que ${nomeAluno}, CPF: ${cpfAluno}`, 20, 50);
  pdf.text("concluiu com êxito a prova de Informática Básica,", 20, 60);
  pdf.text("demonstrando conhecimentos satisfatórios.", 20, 70);
  pdf.text("Bom Jesus das Selvas - MA", 20, 90);
  pdf.text(`Data: ${new Date().toLocaleDateString()}`, 20, 100);
  pdf.save("certificado.pdf");
}
