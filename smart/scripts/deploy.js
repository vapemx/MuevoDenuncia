async function main() {
  const denuncia = await ethers.getContractFactory("Denuncia");
  const mensajeHash = ethers.utils.formatBytes32String("mensajeHash"); // Convierte la cadena a bytes32
  const Denuncia = await denuncia.deploy(mensajeHash, 12345);
  
  await Denuncia.deployed();

  console.log("Denuncia desplegada en:", Denuncia.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
