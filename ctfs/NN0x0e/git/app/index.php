<?php
require('./vendor/autoload.php');

print "This form will take the URL of a GitLab repository and display if the repo is readable.\n";
print "Note this is an internal tool for our local 'GitBox' server and wont work on external resources.";

?>

<form method="post" action="/index.php">
  GitLab Repository: <input type="text" name="repourl">
  <input type="submit">

</form>
<!–– I do believe there is a phpinfo display if you developers require. Contact me for additional info if needed. -->

<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  $repourl = $_POST['repourl'];

  if(strpos($repourl, 'http://') !== false){

		print "Sorry we only use HTTPS internally, were super secure like that.";

  } elseif (strpos($repourl, 'GitBox.bigmoneyprojects.internal') !== false) {
	 $git = new CzProject\GitPhp\Git;
	  $readable = $git->isRemoteUrlReadable($repourl, ["refs"]);
	  if($readable){
			print "The GitLab url is readable!";
	  } else {
			print "The GitLab url is not readable!";
	  }

  } else {

		print "Could not process the input. Please provide a URL to the repository.";
  }

}
?>