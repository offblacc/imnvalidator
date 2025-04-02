## Kako lijepo srediti aggregate run unutar validate.py
 - kako uopće javiti "želim pokrenuti sve testove"?
 - dodati samo novu cmdline arg opciju ? - ostali args će se i dalje koristiti no samo ih prosljedi svakom testu
 - sami validate će imati tu logiku u sebi umjesto da sve nezgrapno omotaš s nekim testall...
 - kad se starta sama simulacija ? ovisno o NAČINU POKRETANJA - neka validacija svega bude jedan test po jednoj schemi !! u suprotnom kao dosad
 - dodaj argument --validate-installation
 - makni parallel flag zasad..
 - ako --validate-installation, (postavi flag u config?), ..

## 2 načina rada
### Obični validate
 - Započinje simulaciju odmah
 - test file i config file dobiva kao cmdline args
### Validate installation
 - Započinje simulaciju za svaki test
 - test file i config file dobiva iteriranjem kroz direktorije u tests/


## Razno
 - možda odvoji trenutnu logiku, logiku vezanu uz par schema - config u zasebnu funkciju ili nešto, ove glavne dijelove:
   - validacija json_config datoteke
   - check nodes exist
   - samu parallel/sequential logiku pokretanja
