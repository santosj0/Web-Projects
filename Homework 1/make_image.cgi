#!/usr/bin/perl

# Author: James Santos
# Objective: Display an image via parameters provided.

use strict;
use CGI qw/:standard/;
use GD;
use List::Util qw(max);

# Displays error picture
sub error {
	my $error 	= $_[0];
	my $color 	= $_[1];	

	$error->stringFT($color,
			 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
		 	 200,
			 0,
		 	 200, 575,
		 	 "Error");
}

# Scales a number
sub scale {

	my $num 	= $_[0];
	my $range 	= $_[1];
	my @range	= @$range;
	my $min_t 	= $_[2];
	my $max_t 	= $_[3];

	my $min 	= 1;
	my $max 	= max @range;

	return int((($num - $min) / ($max - $min)) * ($max_t - $min_t) + $min_t);
	
}

# Places the content type to png
print header(-type=>'image/png');

# Image creation and colors
my $image 	= new GD::Image(1000, 1000);
my $background 	= $image->colorAllocate(0, 0, 0);
my $blue 	= $image->colorAllocate(0, 0, 255);
my $red 	= $image->colorAllocate(255, 0, 0);
my $green	= $image->colorAllocate(0, 255, 0);

# Get Parameters
if(param())
{

	# Get the parameters
	my $height 		= param('height');
	my $width 		= param('width');
	my $diameter 		= param('radius') * 2;
	my $shape 		= param('shape');
	my @param 		= multi_param('parameters');

	# Generates lists for scaling
	my @hw			= ($height, $width);
	my @di			= ($diameter);

	# Scales to desired height, width, and diameter
	my $new_height 		= scale($height, \@hw, 1, 800);
	my $new_width		= scale($width, \@hw, 1, 800);
	my $new_diameter	= scale($diameter, \@di, 1, 800);

	# Starting Position
	my $x 			= int(((800 - $new_width) / 2) + 100);
	my $y 			= int(((800 - $new_height) / 2) + 100);

	# Triangle Section
	if($shape eq "triangle"
		and grep { $_ eq "right triangle"} @param )
	{
		# Generates the triangle
		my $triangle 	= new GD::Polygon;

		# Adds the points to the canvas
		$triangle->addPt($x, $y);
		$triangle->addPt($x, $y + $new_height);
		$triangle->addPt($x + $new_width, $y + $new_height);

		# Fills the triangle with color
		$image->filledPolygon($triangle, $blue);

		# Adds Width
		$image->stringFT($green,
				 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
			 	 30,
			 	 0,
			 	 $x,
			 	 $y + $new_height + 50,
			 	 $width);

		# Adds Height
		$image->stringFT($red,
				 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
				 30,
				 3.1415/2,
				 $x - 5,
				 $y + $new_height,
				 $height);

	}

	# Rectangle Section
	if($shape eq "rectangle")
	{
		# Generates the rectangle
		$image->filledRectangle($x, $y, $x + $new_width, $y + $new_height, $blue);

		# Add Width
		$image->stringFT($green,
				 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
				 30,
				 0,
				 $x - 5,
				 $y - 5,
				 $width);

		# Add Height
		$image->stringFT($red,
				 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
				 30,
				 3.1415/2,
				 $x - 5,
				 $y + $new_height,
				 $height);
	}

	# Circle Section
	if($shape eq "circle")
	{
		# Generates the circle
		$image->arc(500, 500,
			    $new_diameter, $new_diameter,
			    0, 360,
			    $blue);
		
		# Fills the circle
		$image->fill(500, 500, $blue);

		# Add Radius
		$image->stringFT($red,
				 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
				 30,
				 0,
				 460,
				 500 - ($new_diameter / 2),
				 $diameter / 2);

	}

}
else {
	error($image, $red);
}

print $image->png;
