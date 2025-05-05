import Table, { Column } from "../components/Table";
import { useEffect, useState } from "react";
import axios from "axios";

type LogType = {
  ticker: string;
  action: string;
  quantity: number;
  price: number;
  date: string;
  type: string;
  status: "failed" | "polling" | "filled" | "expiry";
  limitPrice: number;
  position_intent: string;
};

const columns: Column<LogType>[] = [
  { key: "ticker", label: "Ticker", sortable: true },
  { key: "action", label: "Action", sortable: true },
  { key: "quantity", label: "Quantity", sortable: true },
  { key: "type", label: "Type", sortable: true },
  { key: "limitPrice", label: "Limit Price", sortable: true },
  { key: "status", label: "Status" },
  { key: "date", label: "Date", sortable: true },
  { key: "position_intent", label: "Position Intent" },
];

function App() {
  const [logs, setLogs] = useState<LogType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const response = await axios.get<LogType[]>(
        "/api/orders/live"
      );
      setLogs(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
    // const interval = setInterval(fetchLogs, 10000); // Auto-refresh every 10 seconds
    // return () => clearInterval(interval); // Cleanup on unmount
  }, []);
  return (
    <div className="w-full min-h-screen pt-10">
      {loading && <div className="text-center">Loading...</div>}
      {error && <div className="text-red-500 text-center">{error}</div>}
      {!loading && !error && (
        <div className="max-w-6xl mx-auto bg-white shadow-lg rounded-lg">
          <Table columns={columns} data={logs} />
        </div>
      )}
    </div>
  );
}

export default App;
