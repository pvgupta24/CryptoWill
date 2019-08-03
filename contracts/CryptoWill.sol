pragma solidity ^0.5.1;

contract CryptoWill {
    address public beneficiary;  // encrypted
    address public owner;
    uint public lastCheckInTime;
    uint public lockInPeriod;
    uint public points = 0;
    mapping(address => address) public wallets;
    
    // mapping(address => unit8) public ---;

    /*constructor*/
    constructor (address walletBeneficiary, address walletOwner) public {
        beneficiary = walletBeneficiary;
        owner = walletOwner;
        uint periodInDays;
        lockInPeriod = periodInDays * 1 days;
        lastCheckInTime = now;
    }

    function() external payable{} // any one can deposit funds directly to the contract address
    
    modifier onlyOwner() {
        require(msg.sender == owner && msg.sender == CryptoWill(owner).getOwner());
        lastCheckInTime = now;
        _;
    }    
    
    modifier OnlyHeir() {
        require(points[msg.sender] != 0);
        _;
    }
    function checkIn() public onlyOwner{} // called by owner periodically to prove he is alive
    
    function setCheckInPeriod(uint periodInDays) public onlyOwner { // called by owner to change check in period
        checkInPeriod = periodInDays * 1 days;
    }

    function sendFunds(address destination, uint amount, bytes data) public onlyOwner { //called by owner to send funds with data to chosen destination
        require(destination.call.value(amount)(data));
    }

    function transferOwnership(address newOwner) onlyOwner { // called by owner to change the ownership
        owner = newOwner;
        beneficiary = owner;
    }
    //called by owner to add/modify an heir; inheritance shares are directly propotional to the points assigned
    function setHeir(address heir, uint8 inheritancePoints, uint periodInDays) onlyOwner returns (address) {
		if (wallets[heir] == 0 && inheritancePoints > 0) {
			//wallets[heir] = factory.create(heir, periodInDays);
		} else if (wallets[heir] > 0 && inheritancePoints == 0) {
			CryptoWill(wallets[heir]).destroy();
			delete wallets[heir];
		}
		totalPoints -= points[wallets[heir]];
		points[wallets[heir]] = inheritancePoints;
		totalPoints += inheritancePoints;
		return wallets[heir];
	}
	/* called by anyone to give the benificiary full ownership of this account when his predecessor is inactive */
	function unlock() {
		require(beneficiary != owner); // already unlocked
		HeritableWallet(owner).claimInheritance();
		owner = beneficiary;
		lastCheckInTime = now;
	}

	/* called by an heir to collect his share in the inheritance */
	function claimInheritance() onlyHeir {
		require (beneficiary == owner); // account is locked
		if (now <= lastCheckInTime + checkInPeriod) throw; // owner was active recently
		uint8 heirPoints = points[msg.sender];
		uint amount = this.balance * heirPoints / totalPoints; // compute amount for current heir
		totalPoints -= heirPoints;
		delete points[msg.sender];
		require(!msg.sender.send(amount)); // transfer proper amount to heir or revert state if it fails
		totalPoints += heirPoints;
		points[msg.sender] = heirPoints;
		if (totalPoints == 0) { // last heir, destroy empty contract
			selfdestruct(owner);
		}
	}
	/* called by owner to terminate this contract */
	function destroy() onlyOwner {
		selfdestruct(owner);
	}
	
	function getOwner() returns (address) { return owner; }
	function getBeneficiary() returns (address) { return beneficiary; }
	
}

