1. Por que no endpoint de retorno HTML eu uso o parâmetro response_class, mas nos outros eu uso o parâmetro response_model?
2. Por que no arquivo de configuração do alembic fica com warming no Settings()?
3. Por que chamar o get_session sem o uso do Depends (do fastapi) dá o erro "AttributeError: 'generator' object has no attribute 'scalar'"
4. Por que o dependency_overrides não é clicável para abrir o local onde ele está assim como os métodos e atributos?
5. Os argumentos mapper e connection da função fake_time_hook não são usados. Por quê?
6. Verificar o warning "ResourceWarning: unclosed database in <sqlite3.Connection object at 0x7f6..." que dá em alguns testes (ex.: test_read_user)
7. Tem como renomear o username do formulário do OAuth?
8. No primeiro exercício da aula 06 diz que o pwdlib não faz validação da senha. Ele não faz mesmo?


# Observações

* Reassistir a aula 04 (1h10m) para entender melhor o mock_db_time
* Assistir live de corrotinas (#151 a #154)
* Reassistir a aula 05 (0h50min) para entender o dependency_overrides