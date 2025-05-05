// components/Table.tsx
import { useState } from "react";

export type Column<T> = {
  key: keyof T;
  label: string;
  sortable?: boolean;
};

type TableProps<T> = {
  columns: Column<T>[];
  data: T[];
};

function Table<T extends Record<string, any>>({ columns, data }: TableProps<T>) {
  const [sortColumn, setSortColumn] = useState<keyof T | null>(null);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const handleSort = (key: keyof T) => {
    if (sortColumn === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(key);
      setSortOrder("asc");
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortColumn) return 0;
    const valA = a[sortColumn];
    const valB = b[sortColumn];

    if (typeof valA === "number" && typeof valB === "number") {
      return sortOrder === "asc" ? valA - valB : valB - valA;
    }

    return sortOrder === "asc"
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });

  return (
    <table className="min-w-full table-auto border-collapse">
      <thead>
        <tr className="bg-gray-100 border-b text-black">
          {columns.map(({ key, label, sortable }) => (
            <th
              key={String(key)}
              className={`px-6 py-3 text-left ${
                sortable ? "cursor-pointer hover:underline" : ""
              }`}
              onClick={() => sortable && handleSort(key)}
            >
              {label}
              {sortable && sortColumn === key && (
                <span className="ml-1">{sortOrder === "asc" ? "↑" : "↓"}</span>
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, idx) => (
          <tr
            key={idx}
            className={`border-b hover:bg-gray-50 text-black ${idx % 2 === 0 ? "bg-gray-50" : ""}`}
          >
            {columns.map(({ key }) => (
              <td key={String(key)} className="px-6 py-4">
                {String(row[key]) === "null" ? "N/A" : String(row[key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Table;
