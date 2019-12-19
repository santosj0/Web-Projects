#!/bin/perl

# Author: James Santos
# Purpose: CGI Script that creates a form to generate an image
# Last Modified: October 1, 2019

# 9/26/2019 Additions:
# - Generated the form
# - Added Result Section

# 10/1/2019 Additions:
# - Modified how p tags work
# - Added a Footer
# - Added Image CGI

# 10/6/2019 Additions:
# - Cleaned up code

use CGI qw/:standard/;			    # CGI Module
use Scalar::Util qw(looks_like_number);     # Determines if variable is a number

# Import Footer
use lib '/templates/';
require Footer;

# Displays the image
sub print_image {
	my $query = $_[0];
	my $shape = $_[1];
	
	print img({
			-src 		=> "./make_image2.cgi?$query",
			-alt 		=> "$shape",
	 		-height		=> '400',
	 		-width 		=> '400'
		});
}

# Validation based on parameter
sub validate {
	my $param = $_[0];
	return not defined $param
	       or not looks_like_number($param)
	       or $param <= 0;
}

# Obtain Query String parameters
my @parameters          = multi_param('parameters');
my $shape               = param('shape');
my $height              = param('height');
my $width               = param('width');
my $radius              = param('radius');
my $query               = query_string();

# Validation - Shape
my $valid_r		= $shape eq "rectangle";
my $valid_t		= $shape eq "triangle";
my $valid_c		= $shape eq "circle";

# Validation - Paramter
my $grep_area		= grep { $_ eq 'area' } @parameters;
my $grep_perimeter	= grep { $_ eq 'perimeter' } @parameters;
my $grep_circumference	= grep { $_ eq 'circumference' } @parameters;
my $grep_right_triangle = grep { $_ eq 'right triangle' } @parameters;

# Validation - Dimension is a number greater than 0
my $valid_height	= looks_like_number($height) and $height > 0;
my $valid_width		= looks_like_number($width) and $width > 0;
my $valid_radius	= looks_like_number($radius) and $radius > 0;

# Builds the website
print header,
      start_html('Generate Image'),
      h1('Image Parameters'),
      
      # Start Form
      start_form,
      h3('Dimensions');
      
      # Height
      print p("Height: ", textfield('height'));
      
      # Invalid Height
      if($query) 
      {
	      if($valid_r or $valid_t)
 	      {
		      if(validate($height))
		      {
			      print "<span style='color: red'> Invalid height!</span>";
		      }
	      }
      }
      
      # Width
      print p("Width: ", textfield('width'));
      
      # Invalid Width
      if($query) 
      {
	      if($valid_r or $valid_t)
	      {
		      if(validate($width))
		      {
			      print "<span style='color: red'> Invalid width!</span>";
		      }
	      }
      }
      
      #Radius
      print p("Radius: ", textfield('radius'));
      
      # Invalid Radius
      if($query)
      {
	      if($valid_c)
	      {
		      if(validate($radius))
	 	      {
			      print "<span style='color: red'> Invalid radius!</span>";
		      }
	      }
      }
      
      # Shape
      print h3('Shape'),
      	    radio_group(-name=>'shape',
		    	-values=>['rectangle', 'circle', 'triangle'],
		    	-default=>['rectangle']);

      # Invalid Shape
      if($query)
      {
	      if( not ($valid_r or $valid_t or $valid_c) )
	      {
		      print "<span style='color: red'> Invalid shape!</span>";
	      }
      }      

      # Parameters	
      print h3('Parameters'),
	    checkbox_group(-name=>'parameters',
			   -values=>['right triangle', 'area', 
				     'perimeter', 'circumference'],
			   -defaults=>['area', 'perimeter']);

      # Invalid Parameters
      if($query)
      {
	      if(@parameters)
	      {
		      if( not($grep_right_triangle or $grep_area or $grep_perimeter or $grep_circumference) )
		      {
			      print "<span style='color: red'> Invalid Parameter</span>";
		      }
	      }
      }

      # Finished Form
      print br, 
      	    br, 
	    submit, 
	    end_form;

# Displays results if there is a query string
if($query)
{
	print hr;
	print h1('Results');

	# Display shape
	if($valid_r or $valid_t or $valid_c)
	{
		print p("Shape: ", em($shape));
	}

	# Invalid Shape
	if(not ($valid_r or $valid_t or $valid_c) )
	{
		print p("Please specify a valid shape.");
	}

	# Invalid Parameter
	if(not ($grep_right_triangle or $grep_area or $grep_perimeter or $grep_circumference) )
	{
		print p("Please specify a valid parameter.");
	}

	# Rectangle Section
	if($valid_r and $valid_height and $valid_width)
	{
		# Display Area
		if($grep_area)
		{
			print p("Area: ", em(sprintf("%.3f", $height * $width)));
		}

		# Display Perimeter
		if($grep_perimeter)
		{
			print p("Perimeter: ", em(sprintf("%.3f", 2*($height + $width))));
		}

		# Display Image
		print_image($query, $shape);
		
	}

	# Rectangle/Triangle Error
	if($valid_r or $valid_t)
	{
		if(not defined $height 
			or not defined $width 
			or not $valid_height
			or not $valid_width)
		{
			print p("Please specify a valid height or width.");
		}

		if($height <= 0)
		{
			print p("Height needs to be greater than 0.");
		}

		if($width <= 0)
		{
			print p("Width needs to be greater than 0.");
		}

		if($valid_t)
		{
			if(not $grep_right_triangle)
			{
				print p("Only right triangles allowed.");
			}
		}
	}

	# Circle Section
	my $pi = 3.1415;
	
	if($valid_c and $valid_radius)
	{
		# Display Area
		if($grep_area)
		{
			print p("Area: ", em(sprintf("%.3f",$pi * ($radius ** 2))));
		}

		# Display Circumference
		if($grep_circumference)
		{
			print p("Circumference: ", em(sprintf("%.3f", 2 * $pi * $radius)));
		}

		# Display Image
		print_image($query, $shape);
	}
		
	# Circle Error
	if($valid_c)
	{
		if(not defined $radius or not $valid_radius)
		{
			print p("Please specify a valid radius.");
		}

		if($radius <= 0)
		{
			print p("Radius needs to be greater than 0.");
		}
	}

	# Triangle Section
	if($valid_t and $valid_height and $valid_width and $grep_right_triangle)
	{
		# Display Area
		if($grep_area)
		{
			print p("Area: ", em(($height * $width) / 2));
		}

		# Display Perimeter
		if($grep_perimeter)
		{
			print p("Perimeter: ", em(sprintf("%.3f", $width + $height + sqrt(($width ** 2) + ($height ** 2)))));
		}

		# Display Image
		print_image($query, $shape);
	}

}

# Footer
print Footer::print_footer();

print end_html;
