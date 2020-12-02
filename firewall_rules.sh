# firewall configuration script
echo "Script Started: at "$(date)
ufw_pkg='ufw'
# Check if ufw is installed
if [ $(dpkg-query -W -f='${Status}' $ufw_pkg 2>/dev/null | grep -c "ok installe$
then
   sudo yum install -y $ufw_pkg
else
   echo "****** ufw is installed ******"
fi

sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
# enable firewall service and reload
sudo ufw enable
sudo ufw reload
echo "Script Finished: at "$(date)
