#!/usr/bin/perl -w

# --------------------------------------------------
# ARGV[0] = <hostname>     required
# ARGV[1] = <snmp port>    required
# ARGV[2] = <community>    required
# ARGV[3] = <version>      required
# --------------------------------------------------
use Net::SNMP;

# verify input parameters
my $in_hostname         = $ARGV[0] if defined $ARGV[0];
my $in_port             = $ARGV[1] if defined $ARGV[1];
my $in_community        = $ARGV[2] if defined $ARGV[2];
my $in_version          = $ARGV[3] if defined $ARGV[3];
my $in_critical         = $ARGV[4] if defined $ARGV[4];
my $in_warning          = $ARGV[5] if defined $ARGV[5];
my $value;
# usage notes
if (
        ( ! defined $in_hostname ) ||
        ( ! defined $in_port ) ||
        ( ! defined $in_community ) ||
        ( ! defined $in_version )
        ) {
        print   "usage:\n\n
                $0 host port community version critic_temp warning_level\n\n";
        exit;
}

die "Warning level MUST be < critical" if ($in_warning >= $in_critical);

# list all OIDs to be queried
my $temp      = ".1.3.6.1.4.1.26143.1.4.1.2.4.116.101.109.112.1";

# Special parameters
my $in_delay            = 3; #DTH need 2 seconds to reset: it does not accept more than 1 query every 2 seconds.

# get information via SNMP
# create session object
my ($session, $error) = Net::SNMP->session(
                        -hostname      => $in_hostname,
                        -port          => $in_port,
                        -version       => $in_version,
                        -community     => $in_community,
                        # please add more parameters if there's a need for them:
                        #   [-localaddr     => $localaddr,]
                        #   [-localport     => $localport,]
                        #   [-nonblocking   => $boolean,]
                        #   [-domain        => $domain,]
                        #   [-timeout       => $seconds,]
                        #   [-retries       => $count,]
                        #   [-maxmsgsize    => $octets,]
                        #   [-translate     => $translate,]
                        #   [-debug         => $bitmask,]
                        #   [-username      => $username,]    # v3
                        #   [-authkey       => $authkey,]     # v3
                        #   [-authpassword  => $authpasswd,]  # v3
                        #   [-authprotocol  => $authproto,]   # v3
                        #   [-privkey       => $privkey,]     # v3
                        #   [-privpassword  => $privpasswd,]  # v3
                        #   [-privprotocol  => $privproto,]   # v3
                        );

# on error: exit
if (!defined($session)) {
        printf("ERROR: %s.\n", $error);
        exit 1;
        }

# perform get requests for all wanted OIDs
my $result = $session->get_request(
                         -varbindlist      => [ $temp ],
                       );

# Whait senseor reset (2s)
#sleep(3);

$session->close;

# print results
#printf("%s", #
#        $result->{$temp},
#        );

#print "Literal: $result->{$temp}\n";

($value) = $result->{$temp} =~ /(\d+\.\d*)/;
#$value  =~ /(\d+)/;
#print "Temp= $value\n";

if ($value < $in_warning)
{
    print "Temp under limits ($in_warning)\n";
    exit 0;
}
elsif (($value > $in_warning) && ($value < $in_critical))
{
    print "Temp $value over $in_warning, but not over critical ($in_critical)\n";
    exit 1;
}
elsif ($value >= $in_critical)
{
    print "Critical!!! temp is over $in_critical\n";
    exit 2;
}
else
{
    print "UNKNOWN Unable to determine the temperature. \n";
    exit 3; #Exit code 3 is what tells Nagios the check has no clue.

