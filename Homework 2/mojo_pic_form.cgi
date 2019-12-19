#!/usr/bin/perl

# Author: James Santos
# Purpose: Mojolicious Application that mirrors the CGI script
# Last Modified: October 5, 2019

# 10/5/2019
# - Generated the routes
# - Generated the form template
# - Created validators
# - Added validators
# - Added form validators
# - Generated the results partial template

# 10/6/2019
# - Cleaning up code
# - Modified image to use make_image2.cgi instead of make_image.cgi
# - Fix conversion issue of empty hash_map to use every_param instead

# Imports the Mojolicious Lite Package
# Automatically enables "strict", "warnings", "utf8", and perl 5
use Mojolicious::Lite; 

# Imports the Validator Package
use Mojolicious::Validator;

# Imports the looks_like_number function
use Scalar::Util qw(looks_like_number);

# Custom Validators
# Checks if array contains the specified word
app->validator->add_check(
	contains => sub {
		my ($v, $name, $value, $comparator) = @_;

		# Grabs list reference and converts to usable array
		my $ep 		= $v->every_param($name);
		my @list 	= @$ep;	

		return not grep { $_ eq $comparator } @list;
	}
);

# Makes sure that the dimensions/parameters are valid depending on the shape
app->validator->add_check(
	valid_shape => sub {
		my ($v, $name, $value) = @_;

		# Makes sure only shape is passed
		if(not $name eq 'shape'){ return 1; }

		# Rectangle Section
		if($value eq 'rectangle'){
			$v->required('height')->num(1, undef);
			$v->required('width')->num(1, undef);
		}

		# Circle Section
		if($value eq 'circle'){
			$v->required('radius')->num(1, undef);
		}

		# Triangle Section
		if($value eq 'triangle'){
			$v->required('height')->num(1, undef);
			$v->required('width')->num(1, undef);
			$v->required('parameters')->contains('right triangle');
		}

		return $v->has_error;

	}
);

# Route to the home page
# URL: /mojo_pic_form.cgi
get '/' => sub {
	# Mojo Controller/Validator
	my $c 		= shift;
	my $v 		= $c->validation;

	# Parameters
	my $height 	= $c->param('height');
	my $width 	= $c->param('width');
	my $radius	= $c->param('radius');
	my $shape 	= $c->param('shape');
	my @param	= $c->every_param('parameters');

	# Passes general variables to template
	$c->stash(c => $c);

	# Renders the html page if no parameters are passed
	return $c->render(template => 'form') unless $v->has_data;

	# Validation area	
	# Makes sure parameters is only those four options
	$v->optional('parameters')->in('right triangle', 'area', 'perimeter', 'circumference');

	# Makes sure everything is valid
	$v->required('shape')->in('rectangle', 'circle', 'triangle')->valid_shape;

	# Render the html page if it has errors
	return $c->render(template => 'form') if $v->has_error;

	# Passed all validation
	$c->render(template => 'form');



} => 'form';

app->start;
__DATA__

@@ form.html.ep
<!DOCTYPE html>
<html>
<head>
	<title>Generate Image</title>
	<style>
		span {
			color: red;
		}
	</style>
</head>
<body>
	<h1>Image Parameters</h1>
	%= form_for '/' => begin
	%# Dimensions
	<h3>Dimensions</h3>

	<p>
	%# Height
	%= label_for height => "Height: "
	%= text_field 'height'

	%# Height Error
	% if (my $err = validation->error('height')) {
		<span>
			%= 'Value is required.' if $err->[0] eq 'required'
			%= 'Value needs to be a number greater than 0.' if $err->[0] eq 'num'
		</span>
	% }
	</p>

	<p>
	%# Width
	%= label_for width => "Width: "	
	%= text_field 'width'
	
	%# Width Error
	% if (my $err = validation->error('width')) {
		<span>
			%= 'Value is required.' if $err->[0] eq 'required'
			%= 'Value needs to be a number greater than 0.' if $err->[0] eq 'num'
		</span>
	% }
	</p>		

	<p>
	%# Radius
	%= label_for radius => "Radius: "
	%= text_field 'radius'
	
	%# Radius Error
       	% if (my $err = validation->error('radius')){
		<span>
			%= 'Value is required.' if $err->[0] eq 'required'
			%= 'Value needs to be a number greater than 0.' if $err->[0] eq 'num'
		</span>
	% }	
	</p>

	%# Shape
	<h3>Shape</h3>
	%= radio_button shape => 'rectangle', checked => "checked"
	%= label_for shape => 'rectangle'
	%= radio_button shape => 'circle'
	%= label_for shape => "circle"
	%= radio_button shape => 'triangle'
	%= label_for shape => "triangle"

	%# Shape Error
	% if (my $err = validation->error('shape')){
		<span>
			%= 'Please select one of these choices.' if $err->[0] eq 'in'
		</span>
	% }

	%# Parameters
	<h3>Parameters</h3>
	%= check_box parameters => 'right triangle'
	%= label_for parameters => 'right triangle'
	%= check_box parameters => 'area'
	%= label_for parameters => 'area'
	%= check_box parameters => 'perimeter'
	%= label_for parameters => 'perimeter'
	%= check_box parameters => 'circumference'
	%= label_for parameters => 'circumference'

	%# Parameters Error
	% if (my $err = validation->error('parameters')){
		<span>
			%= 'Right triangle required.' if ($err->[0] eq 'contains' or $err->[0] eq 'required')
			%= 'Please only choose from the list.' if $err->[0] eq 'in'
		</span>
	% }

	%# Seperator
	<br><br>
	%= submit_button 'Submit'

	%= end

	%# Results Section
	% if (validation->is_valid){
		% if (not validation->has_error) {
			%= include '_results', query => $c->req->query_params
		% }
	% }

	%# Footer
	%= include '_footer'

</body>
</html>

%# Result Section
@@ _results.html.ep
% my $shape = $query->param('shape');
% my $height = $query->param('height');
% my $width = $query->param('width');
% my $radius = $query->param('radius');
% my $ep = $query->every_param('parameters');
% my @parameters = @$ep;

%# Validation
% my $area = grep { $_ eq 'area' } @parameters;
% my $perimeter = grep { $_ eq 'perimeter' } @parameters;
% my $circumference = grep { $_ eq 'circumference' } @parameters;

<hr>

<p>
	Shape: <em><%= $shape %></em>
</p>

%# Rectangle Section
% if($shape eq 'rectangle') {
	
	% if($area) {
		<p>Area: <em><%= ($height * $width) %></em></p>
	% }

	% if($perimeter) {
		<p>Perimeter: <em><%= (2 * $height + 2 * $width) %></em></p>
	% }

% }

%# Circle Section
% if($shape eq 'circle') {
	
	% my $pi = 3.1415;

	% if($area) {
		<p>Area: <em><%= $pi * ($radius**2) %></em></p>
	% }
	
	% if($circumference) {
		<p>Circumference: <em><%= 2 * $pi * $radius %></em></p>
	% }

% }

%# Triangle Section 
% if($shape eq 'triangle') {
	
	% if($area) {
		<p>Area: <em><%= ($height * $width) / 2 %></em></p>
	% }

	% if($perimeter) {
		<p>Perimeter: <em><%= $height + $width + sqrt($height**2 + $width**2) %></em></p>
	% }

% }

%# Apply the imag
%= image 'http://elvis.rowan.edu/~santosj0/awp/homework1/make_image.cgi?'.$query, alt => 'Generated Image', height => 400, width => 400

%# Footer
@@ _footer.html.ep
% use lib '/home/santosj0/public_html/awp/templates/';
% require Footer;
%== Footer::print_footer();
