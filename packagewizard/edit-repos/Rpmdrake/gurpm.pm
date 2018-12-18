package Rpmdrake::gurpm;
#*****************************************************************************
#
#  Copyright (c) 2002 Guillaume Cottenceau
#  Copyright (c) 2002-2007 Thierry Vignaud <tvignaud@mandriva.com>
#  Copyright (c) 2003, 2004, 2005 MandrakeSoft SA
#  Copyright (c) 2005-2007 Mandriva SA
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2, as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#*****************************************************************************
#
# $Id: gurpm.pm 248121 2008-10-11 11:19:36Z tv $


use lib qw(/usr/lib/libDrakX);
use mygtk2 qw(gtknew);  #- do not import anything else, especially gtkadd() which conflicts with ugtk2 one
use ugtk2 qw(:all);
use base qw(ugtk2);


sub new {
    my ($self, $title, $initializing, %options) = @_;
    my $mainw = bless(ugtk2->new($title, %options, default_width => 600, width => 600), $self);
    $::main_window = $mainw->{real_window};
    $mainw->{label} = gtknew('Label', text => $initializing, alignment => [ 0.5, 0 ]);
    # size label's heigh to 2 lines in order to prevent dummy vertical resizing:
    my $context = $mainw->{label}->get_layout->get_context;
    my $metrics = $context->get_metrics($mainw->{label}->style->font_desc, $context->get_language);
    $mainw->{label}->set_size_request(-1, 2 * Gtk2::Pango->PANGO_PIXELS($metrics->get_ascent + $metrics->get_descent));

    $mainw->{progressbar} = gtknew('ProgressBar');
    gtkadd($mainw->{window}, $mainw->{vbox} = gtknew('VBox', spacing => 5, border_width => 6, children_tight => [
        $mainw->{label},
        $mainw->{progressbar}
    ]));
    mygtk2::enable_sync_flush($mainw->{rwindow});
    $mainw->{rwindow}->set_position('center-on-parent');
    $mainw->{real_window}->show_all;
    mygtk2::sync_flush($mainw->{rwindow});
    $mainw;
}

sub label {
    my ($self, $label) = @_;
    $self->{label}->set($label);
    select(undef, undef, undef, 0.1);  #- hackish :-(
    $self->flush;
}

sub progress {
    my ($self, $fraction) = @_;
    $fraction = 0 if $fraction < 0;
    $fraction = 1 if 1 < $fraction;
    $self->{progressbar}->set_fraction($fraction);
    $self->flush;
}

sub DESTROY {
    my ($self) = @_;
    mygtk2::may_destroy($self);
    $self and $self->destroy;
    $self = undef;
    $self->{cancel} = undef;  #- in case we'll do another one later
}

sub validate_cancel {
    my ($self, $cancel_msg, $cancel_cb) = @_;
    if (!$self->{cancel}) {
        gtkpack__(
	    $self->{vbox},
	    $self->{hbox_cancel} = gtkpack__(
		gtknew('HButtonBox'),
		$self->{cancel} = gtknew('Button', text => $cancel_msg, clicked => \&$cancel_cb),
	    ),
	);
    }
    $self->{cancel}->set_sensitive(1);
    $self->{cancel}->show;
}

sub invalidate_cancel {
    my ($self) = @_;
    $self->{cancel} and $self->{cancel}->set_sensitive(0);
}

sub invalidate_cancel_forever {
    my ($self) = @_;
    $self->{hbox_cancel} or return;
    $self->{hbox_cancel}->destroy;
    # FIXME: temporary workaround that prevents
    # Gtk2::Label::set_text() set_text_internal() -> queue_resize() ->
    # size_allocate() call chain to mess up when ->shrink_topwindow()
    # has been called (#32613):
    #$self->shrink_topwindow;
}

1;
