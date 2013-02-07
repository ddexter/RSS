<html>
  <body>
    <?php
    require_once 'Config/Lite.php'

    $THREE_DAYS_SEC = 259200;

    $threeDaysAgo = time() - $THREE_DAYS_SEC;

    # Be sure you include the same RSS.ini file for python somewhere that is RO
    $ini = new Config_Lite("/home2/debatepr/RSS.ini");
    $db = $ini->get('Database', 'database');
    $host = $ini->get('Database', 'host');
    $user = $ini->get('Database', 'user');
    $password = $ini->get('Database', 'password');

    $con = pg_connect("host=$host dbname=$db user=$user password=$password") or die;
    $query = "SELECT * FROM rssfeed WHERE pubDate >= to_timestamp($threeDaysAgo) ORDER BY pubDate DESC";
    $res = pg_query($con, $query) or die;
    while ($row = pg_fetch_assoc($res)) {
      echo $row['pubDate'];
    }
    pg_close($con);
    ?>
  </body>
</html>
