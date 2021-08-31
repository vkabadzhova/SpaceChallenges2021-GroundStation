<?php include_once('head.php')?>

<?php include_once('navigation.php')?>



<section class="d-flex justify-content-center w-100">
	<div class="col-6">
		<form>
			<label>Select Target Satellite:</label>
			<div class="dropdown">
				<button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
					Dropdown button
				</button>
				<ul class="dropdown-menu pt-0" aria-labelledby="dropdownMenuButton1">
					<li class="d-flex">
						<input class="form-control" style="border-radius:0px" type="search" placeholder="Search" aria-label="Search">
						<button class="btn border-bottom rounded-none" type="submit">Search</button>
					</li>
					<li><a class="dropdown-item" href="#">Action</a></li>
					<li><a class="dropdown-item" href="#">Another action</a></li>
					<li><a class="dropdown-item" href="#">Something else here</a></li>
				</ul>
			</div>
		</form>
	</div>

</section>

<?php include_once('foot.php')?>