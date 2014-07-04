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
# usage notes
if (
        ( ! defined $in_hostname ) ||
        ( ! defined $in_port ) ||
        ( ! defined $in_community ) ||
        ( ! defined $in_version )
        ) {
        print   "usage:\n\n
                $0 &lt;host&gt; &lt;port&gt; &lt;community&gt; &lt;version&gt;\n\n";
        exit;
}

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


# print results
printf("%s", #
        $result->{$temp},
        );

$session->close;
