import flet as ft
import requests

API_BASE_URL = "LINK_DA_API"


def main(page: ft.Page):
    page.title = "Flet App"

    #Criar Aluno aba
    nome_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="Email")
    faixa_field = ft.TextField(label="Faixa ( B, A, R, M, P)")
    data_field = ft.TextField(label="Data de Nascimento (YYYY-MM-DD)")
    create_result = ft.Text()
    
    def criar_aluno(e):
       payload = {
           "nome": nome_field.value,
           "email": email_field.value,
           "faixa": faixa_field.value,
           "data_nascimento": data_field.value
       }

       response = requests.post(API_BASE_URL + "/", json=payload)
       if response.status_code == 200:
           aluno = response.json()
           create_result.value = f"Aluno criado com sucesso: {aluno}"
       else:
           create_result.value = f"Erro ao criar aluno: {response.text}"
    
       page.update()
       
       print(payload)

    create_button = ft.ElevatedButton(text="Criar Aluno", on_click=criar_aluno)

    criar_aluno_tab = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_field,
            create_result,
            create_button,
        ],
        scroll=True
    )

    #Listar Alunos aba
    students_table = ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Faixa")),
            ft.DataColumn(ft.Text("Data de Nascimento")),
        ],
        rows = []
    )

    list_result = ft.Text()

    def listar_aluno(e):
        response = requests.get(API_BASE_URL + "/alunos/")
        alunos = response.json()

        students_table.rows.clear()

        for aluno in alunos:
            row = ft.DataRow(
                cells= [
                    ft.DataCell(ft.Text(aluno.get('nome'))),
                    ft.DataCell(ft.Text(aluno.get('email'))),
                    ft.DataCell(ft.Text(aluno.get('faixa'))),
                    ft.DataCell(ft.Text(aluno.get('data_nascimento'))),


                ]
            )
            students_table.rows.append(row)
        list_result.value = f"{len(alunos)} alunos listados"

        page.update()

    list_button = ft.ElevatedButton(text="Listar Alunos", on_click=listar_aluno)

    listar_aluno_tab = ft.Column(
        [
            students_table, list_result,list_button,
        ],
        scroll=True
    )


    #Adicionar Aulas aba

    email_aula_field = ft.TextField(label="Email do Aluno")
    qtd_filed = ft.TextField(label="Quantidade de Aulas", value = "1")
    aula_result = ft.Text()

    def marcar_aula_click(e):
        payload = {
            "qtd": int(qtd_filed.value),
            "email_aluno": email_aula_field.value
        }

        response = requests.post(API_BASE_URL + "/aula_realizada/", json=payload)

        if response.status_code == 200:
            aula_result.value = f"Aula marcada com sucesso: {response.json()}"
        else:
            aula_result.value = f"Erro ao marcar aula: {response.text}"

        page.update()


    aula_button = ft.ElevatedButton(text="Marcar Aula Realizada",on_click=marcar_aula_click) 
    aula_tab = ft.Column(
        [
            email_aula_field,
            qtd_filed,
            aula_result,
            aula_button
        ],
        scroll=True
    )


    #Progresso Aluno

    email_progress_field = ft.TextField(label="Email do Aluno")
    progress_result = ft.Text()

    def progresso_click(e):
        email = email_progress_field.value
        response = requests.get(API_BASE_URL + "/progresso_aluno/",params={"email_aluno": email})
        if response.status_code == 200:
            progress = response.json()
            progress_result.value = (
                f'Nome: {progress.get("nome")}\n'
                f'Email: {progress.get("email")}\n'
                f'Faixa: {progress.get("faixa")}\n'
                f'Total de Aulas: {progress.get("total_aulas")}\n'
                f'Aulas necessárias prox faixa: {progress.get("aulas_necessarias_para_prox_faixa")}\n'
                
            )
        else:
            progress_result.value = f"Erro ao obter progresso: {response.text}"
        print(response.json())

        page.update()


    progress_button = ft.ElevatedButton(text="Ver Progresso", on_click=progresso_click)

    progress_tab = ft.Column(
        [
        email_progress_field,
        progress_result,
        progress_button
        ],
        scroll=True
    )


    #Atualizar Aluno 
    aluno_id_field = ft.TextField(label="ID do Aluno")
    nome_update_field = ft.TextField(label="Novo Nome")
    email_update_field = ft.TextField(label="Novo Email")
    faixa_update_field = ft.TextField(label="Nova Faixa")
    data_update_field = ft.TextField(label="Nova Data de Nascimento (YYYY-MM-DD)")
    update_result = ft.Text()

    def update_aluno(e):
        
        aluno_id = aluno_id_field.value
        if not aluno_id:
            update_result.value = "ID do aluno é necessário."
        else:
            payload = {
                "nome": nome_update_field.value,
                "email": email_update_field.value,
                "faixa": faixa_update_field.value,
                "data_nascimento": data_update_field.value
            }

            print(payload)
            response = requests.put(API_BASE_URL + f"/alunos/{aluno_id}", json=payload)
            if response.status_code == 200:
                aluno = response.json()
                update_result.value = f"Aluno atualizado: {aluno}"
            else:
                update_result.value = f"Erro: {response.text}"
        
        page.update()

    update_button = ft.ElevatedButton(text="Atualizar Aluno", on_click=update_aluno)
    update_tab = ft.Column(
        [
            aluno_id_field,
            nome_update_field,
            email_update_field,
            faixa_update_field,
            data_update_field,
            update_result,
            update_button
        ],
        scroll=True
    )


    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Criar Aluno", content=criar_aluno_tab),
            ft.Tab(text="Listar Alunos", content=listar_aluno_tab),
            ft.Tab(text="Adicionar Aulas", content=aula_tab),
            ft.Tab(text="Progresso do Aluno", content=progress_tab),
            ft.Tab(text="Atualizar Aluno", content=update_tab)
        ],
    )


    page.add(tabs)

    
if __name__ == "__main__":
    ft.app(target=main)

