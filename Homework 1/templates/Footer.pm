#!/usr/bin/perl

package Footer;

sub print_footer {
	return "<footer>
		<hr />
		<a href='http://elvis.rowan.edu/~santosj0/awp/'
			title='Link to AWP page'>
			J. Santos
		</a>

		<span style='float: right'>
		<a href='http://validator.w3.org/check/referer'>HTML5</a> / 
		<a href='http://jigsaw.w3.org/css-validator/check/referer?profile=css3'>CSS3</a>
		</span>
		</footer>"
}

1;
