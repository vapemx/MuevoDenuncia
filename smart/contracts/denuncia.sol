// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract Denuncia {
    string public mensajeHash;
    string public fecha;
    bool public status;
    address public firmadoPor;

    constructor(string memory _mensajeHash, string memory _fecha) {
        mensajeHash = _mensajeHash;
        fecha = _fecha;
        status = false;
        firmadoPor = address(0);
    }

    function firmarContrato(string memory _mensajeHash, string memory _fecha) external {

        mensajeHash = _mensajeHash;
        fecha = _fecha;
        firmadoPor = msg.sender;
        status = true;
    }

    function resolverDenuncia() external {
        require(status, "");
        require(msg.sender == owner(), "Solo el propietario puede resolver la denuncia");
        status = false;
    }

    function owner() public view returns(address) {
        return address(this);
    }
}
