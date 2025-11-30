import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Sun, Cloud, CloudRain, Wind, Droplets, Thermometer, MapPin } from "lucide-react";
import { format } from "date-fns";

interface WeatherData {
  temp: number;
  condition: "sunny" | "cloudy" | "rainy";
  humidity: number;
  wind: number;
}

const WeatherHeader = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [weather] = useState<WeatherData>({
    temp: 24,
    condition: "sunny",
    humidity: 65,
    wind: 12,
  });

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  const getWeatherIcon = () => {
    switch (weather.condition) {
      case "sunny":
        return <Sun className="w-5 h-5 text-farm-sun" />;
      case "cloudy":
        return <Cloud className="w-5 h-5 text-muted-foreground" />;
      case "rainy":
        return <CloudRain className="w-5 h-5 text-farm-sky" />;
      default:
        return <Sun className="w-5 h-5 text-farm-sun" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="w-full py-2 px-4"
    >
      <div className="max-w-6xl mx-auto">
        {/* Weather Widget Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="inline-flex items-center gap-3 px-4 py-2 rounded-2xl bg-card/80 backdrop-blur-sm border border-border/50 shadow-sm"
        >
          {/* Location */}
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground pr-3 border-r border-border/50">
            <MapPin className="w-3.5 h-3.5" />
            <span className="font-medium">Your Farm</span>
          </div>

          {/* Date */}
          <div className="text-xs text-muted-foreground pr-3 border-r border-border/50">
            {format(currentTime, "EEE, MMM d")}
          </div>

          {/* Weather Condition + Temp */}
          <div className="flex items-center gap-2">
            {getWeatherIcon()}
            <div className="flex items-center gap-1">
              <Thermometer className="w-3.5 h-3.5 text-destructive/70" />
              <span className="text-sm font-semibold text-foreground">{weather.temp}°C</span>
            </div>
          </div>

          {/* Humidity */}
          <div className="hidden sm:flex items-center gap-1.5">
            <Droplets className="w-3.5 h-3.5 text-farm-sky" />
            <span className="text-xs font-medium text-muted-foreground">{weather.humidity}%</span>
          </div>

          {/* Wind */}
          <div className="hidden md:flex items-center gap-1.5">
            <Wind className="w-3.5 h-3.5 text-muted-foreground" />
            <span className="text-xs font-medium text-muted-foreground">{weather.wind} km/h</span>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default WeatherHeader;
