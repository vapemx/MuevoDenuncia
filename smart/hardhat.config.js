/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("@nomiclabs/hardhat-etherscan");
require("@nomiclabs/hardhat-web3");
require("@nomicfoundation/hardhat-toolbox");


const INFURA_API_KEY = "af40d34f98974ade80b966854549e5ad";

const SEPOLIA_PRIVATE_KEY = "99a240e516f80711bb3bf60f1fcddb821a3a22237cba13989214a4d6918c171d";

module.exports = {
  solidity: "0.8.9",
  networks: {
    sepolia: {
      url: `https://sepolia.infura.io/v3/${INFURA_API_KEY}`,
      accounts: [SEPOLIA_PRIVATE_KEY]
    }
}
};
