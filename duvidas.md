1. Por que no endpoint de retorno HTML eu uso o parâmetro response_class, mas nos outros eu uso o parâmetro response_model?
2. Por que no arquivo de configuração do alembic fica com warming no Settings()?
3. Por que chamar o get_session sem o uso do Depends (do fastapi) dá o erro "AttributeError: 'generator' object has no attribute 'scalar'"
4. Por que o dependency_overrides não é clicável para abrir o local onde ele está assim como os métodos e atributos?
5. Os argumentos mapper e connection da função fake_time_hook não são usados. Por quê?
6. Verificar o warning "ResourceWarning: unclosed database in <sqlite3.Connection object at 0x7f6..." que dá em alguns testes (ex.: test_read_user)
7. Tem como renomear o username do formulário do OAuth?
8. No primeiro exercício da aula 06 diz que o pwdlib não faz validação da senha. Ele não faz mesmo?
9. Se eu usar user_db = await session.scalar(
            select(User).where(User.username == new_user.username)
        ), eu tomo o seguinte erro: test_create_user - sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place?, mas se eu deixar ...where(User.username == 'test'), o teste passa
10. na nossa aplicação assíncrona, por que a migração precisa ser assíncrona também? a aplicação vai rodar durante uma migração?
11. qual a diferença de função assíncrona para corrotina?


# Observações

* Reassistir a aula 04 (1h10m) para entender melhor o mock_db_time
* Assistir live de corrotinas (#151 a #154)
* Reassistir a aula 05 (0h50min) para entender o dependency_overrides
* Assistir live de faker e factory-boy (#281)
* 