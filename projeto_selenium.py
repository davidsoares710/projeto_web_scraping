from seleniumbase import SB
import pandas as pd


def fazer_login(sb):
    """Abre o site e realiza o login com as credenciais fornecidas."""
    sb.open("https://www.saucedemo.com/")
    sb.type("#user-name", "standard_user")
    sb.type("#password", "secret_sauce")
    sb.click("#login-button")
    sb.wait_for_element(".inventory_list")
    print("Login realizado com sucesso.")


def coletar_produtos(sb):
    """Coleta nome, descrição e preço de todos os produtos da loja."""
    produtos = []
    itens = sb.find_elements(".inventory_item")

    for item in itens:
        nome = item.find_element("css selector", ".inventory_item_name").text
        descricao = item.find_element("css selector", ".inventory_item_desc").text
        preco = item.find_element("css selector", ".inventory_item_price").text

        produtos.append({
            "Nome": nome,
            "Descricao": descricao,
            "Preco": preco
        })

    print(f"Produtos coletados: {len(produtos)}")
    return produtos


def salvar_csv(produtos):
    """Salva os dados dos produtos em um arquivo CSV."""
    df = pd.DataFrame(produtos)
    df.to_csv("produtos.csv", index=False, encoding="utf-8-sig")
    print("Arquivo produtos.csv salvo com sucesso.")


def adicionar_ao_carrinho(sb):
    """Adiciona todos os produtos disponíveis ao carrinho."""
    botoes = sb.find_elements("button.btn_inventory")
    for botao in botoes:
        botao.click()
    print("Todos os produtos adicionados ao carrinho.")


def fazer_checkout(sb):
    """Acessa o carrinho, preenche o formulário e finaliza a compra."""

    # Acessa o carrinho
    sb.click(".shopping_cart_link")
    sb.wait_for_element("#checkout")

    # Inicia o checkout
    sb.click("#checkout")

    # Preenche o formulário com os dados do comprador
    sb.type("#first-name", "Trainee")
    sb.type("#last-name", "PiJunior")
    sb.type("#postal-code", "31270-901")
    sb.click("#continue")

    # Raspa as informações da compra
    pagamento = sb.get_text('[data-test="payment-info-value"]')
    entrega = sb.get_text('[data-test="shipping-info-value"]')
    total = sb.get_text('[data-test="total-label"]')

    print("\nResumo da compra:")
    print(f"  Pagamento : {pagamento}")
    print(f"  Entrega   : {entrega}")
    print(f"  Total     : {total}")

    # Finaliza o pedido
    sb.click("#finish")

    # Verifica a mensagem de confirmação
    mensagem = sb.get_text(".complete-header")
    print(f"\nMensagem de confirmação: {mensagem}")


def main():
    """Função principal que orquestra todo o fluxo do projeto."""
    with SB() as sb:
        fazer_login(sb)
        produtos = coletar_produtos(sb)
        salvar_csv(produtos)
        adicionar_ao_carrinho(sb)
        fazer_checkout(sb)


if __name__ == "__main__":
    main()
