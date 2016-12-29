<?php
$key=$_GET['data'];
$url = "C:\Users\hp1\Desktop\Sentiment_Analyzer";
$images = glob($url."\data\Result_Fetched_Tweets_".$key."*",GLOB_BRACE);
foreach($images as $image)
 {$fill= basename($image);} 
$f = fopen($image, "r");
$i=0;
while (($line = fgetcsv($f)) !== false) 
{
        foreach ($line as $k=>$cell) {
        	if($k==1)
        	{
                $value[$i]=$cell;
            	$i++;

            }
        }
}
?>
<?php
$files = glob($url."\data\Output_Fetched_Tweets_".$key."*",GLOB_BRACE);  
foreach($files as $file)
 {$fil= basename($file);} 
$f = fopen($file, "r");
$cpos=0;
$j=0;
$g=0;
$cneu=0;
$cneg=0;
while (($line = fgetcsv($f)) !== false) 
{
        foreach ($line as $k=>$cell) {
          if($k==0)
          {
            $tweet[$j]=$cell;
            $j++;
          }
          if($k==1)
          {
                $sentiment[$g]=$cell;
              $g++;
            }
        }
}
?>

<html>
<head>
	<title></title>
	<!--<script type="text/javascript" src="sources/jscharts.js">	</script>-->
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	<style type="text/css">
	*
	{
		margin: 0px auto;
		padding:0px;
	}
	.wrapper
	{
		background: url(images/background_image.jpg) no-repeat center center fixed; 
	  background-size: 100vw 100vh;
		/*width: 100%;*/
		/*height: 100%;*/
		overflow: auto;
		background-repeat: none;

	}
	.main
	{
		width: 90%;
		
		border: 5px solid black;
		background-color:rgba(255,255,255,0.84);
		margin: 40px auto;
		padding: 10px;
		padding-bottom: 30px;
		
	}
	input[type=submit]
	{
		width: 70px;
		height: 35px;
		color: white;
		background-color: #008057;
		border: 2px solid white;
		border-radius: 6px;
	}
	input[type=text]
	{
		width:300px;
		height: 30px;
		
	}
	.heading
	{
		margin-top: 20px;
		font-weight: bold;
		font-size: 20px;
		text-align: center;
		font-size: 42px;
	}
	.positive,.negative,.neutral
	{
		width: 80%;
		overflow: auto;
		padding: 5px;
		border: 2px solid black;
		margin-bottom: 5px;
		border-radius: 5px;
	}
	.negative
	{
		background-color: rgba(255,0,0,0.48);
	}
	.positive
	{
		background-color: rgba(23,162,31,0.48);
	}
	.neutral
	{
		background-color: rgba(53,208,227,0.48);


	}

	</style>
</head>
<body onload="fun()">
	
	<div class="wrapper">
		<div class="main">
			
			<p class="heading"><span>Sentiment analysis for </span><span><?php echo $key?></span></p>
			<center><p style="font-size:22px;font-weight:bold;margin-top:32px;">Sentiment by percentage</p></center> 
			<div id="piechart" style="width: 900px; height: 500px; margin:-38px 246px 0px 269px;"></div>
			<script type="text/javascript">
      			google.charts.load('current', {'packages':['corechart']});
      			google.charts.setOnLoadCallback(drawChart);
      			function drawChart() {

        			var data = google.visualization.arrayToDataTable([
          			['Task', 'Hours per Day'],
          			['Positive', <?php echo $value[3] ?>],
          			['Negative',   <?php echo $value[1] ?>],
          			['Neutral', <?php echo $value[2]?>],
          
        			]);


        		var options = {
          			colors: ['#17A21F', '#F70C0C', '#35D0E3'],
          			is3D: true,
          			//legend: {position: 'none'},
          			backgroundColor: { fill:'transparent' },
          			//chartArea:{backgroundColor: { fill: '#FFF',opacity: '0.1'},}
          			
        			};

        		var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        		chart.draw(data, options);
      		}
    		</script>
    		<?php
    		$count=1;
    		do
			{
			$v=rand(1,100);
			/*echo $v;
			echo $tweet[$v];
			echo $sentiment[$v];*/
			if(strcmp($sentiment[$v],"\"positive\"")==0 && $cpos<=3)
			{
				?>
				<div class="positive">
						<p><?php echo $tweet[$v];?></p>
				</div>
				<?php
				$cpos++;
				$count++;
			}
			else if(strcmp($sentiment[$v],"\"negative\"")==0 && $cneg<=3)
			{
				?>
				<div class="negative" >
						<p><?php echo $tweet[$v];?></p>
				</div>
				<?php
				$cneg++;
				$count++;
			}
			else if(strcmp($sentiment[$v],"\"neutral\"")==0 && $cneu<=3)
			{
				?>
				<div class="neutral">
						<p><?php echo $tweet[$v];?></p>
				</div>
				<?php
				$cneu++;
				$count++;
			}
		}while($count<=12);
		?>
			
			 
		</div>
	</div>
	<?php
	fclose($f);
	?>
</body>
</html>