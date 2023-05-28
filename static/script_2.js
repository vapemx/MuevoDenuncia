// Generar intervalos de 30 minutos en el campo de selección de tiempo
var selectTime = document.getElementById("time");
var startTime = new Date();
startTime.setHours(0, 0, 0, 0);
var endTime = new Date();
endTime.setHours(23, 59, 59, 999);
var intervalMinutes = 30;

while (startTime <= endTime) {
    var option = document.createElement("option");
    var timeString = startTime.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
    option.text = timeString;
    option.value = timeString;
    selectTime.appendChild(option);

    startTime.setTime(startTime.getTime() + intervalMinutes * 60000);
}