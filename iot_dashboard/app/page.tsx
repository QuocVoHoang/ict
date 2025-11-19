"use client"

import { AppWindowIcon, CodeIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import Overview from "@/components/Overview/Overview"
import { useState } from "react"
import Devices from "@/components/Devices/Devices"
import Weather from "@/components/Weather/Weather"
import Chart from "@/components/Chart/Chart"
import AlertTab from "@/components/Alert/Alert"

export enum TabType {
  overview = "overview",
  devices = "devices",
  weather = "weather",
  chart = "chart",
  alert = "alert"
}


export default function Home() {
  const [tab, setTab] = useState<TabType>(TabType.overview)

  return (
    <div 
      className={`
        relative min-w-screen min-h-screen bg-cover bg-center 
        ${tab === TabType.overview && 'bg-[url(/living_room2.jpg)]'} 
        ${tab === TabType.devices && 'bg-[url(/house_devices.jpg)]'} 
        ${tab === TabType.weather && 'bg-[url(/house_outside.jpg)]'} 
        ${tab === TabType.chart && 'bg-[url(/utility.jpg)]'} 
        ${tab === TabType.alert && 'bg-[url(/alert.png)]'} 
      `}
    >
      <div className="absolute inset-0 bg-black/40 z-0"></div>

      {/* Nội dung */}
      <div className="relative z-10 p-10 h-screen">
        <Tabs defaultValue={TabType.overview} className="w-full h-full flex flex-col justify-between">
          {/* HEADER */}
          <div className="w-full flex justify-center items-center">
            <TabsList className="w-1/2 font-semibold flex items-center gap-4 bg-black/30">
              <TabsTrigger value={TabType.overview} onClick={() => setTab(TabType.overview)} className="cursor-pointer">
                overview
              </TabsTrigger>
              <TabsTrigger value={TabType.devices} onClick={() => setTab(TabType.devices)} className="cursor-pointer">
                devices
              </TabsTrigger>
              <TabsTrigger value={TabType.weather} onClick={() => setTab(TabType.weather)} className="cursor-pointer">
                weather
              </TabsTrigger>
              <TabsTrigger value={TabType.chart} onClick={() => setTab(TabType.chart)} className="cursor-pointer">
                chart
              </TabsTrigger>
              <TabsTrigger value={TabType.alert} onClick={() => setTab(TabType.alert)} className="cursor-pointer">
                alert
              </TabsTrigger>
            </TabsList>
          </div>

          {/* CONTENT */}
          <div className="w-full">
            <TabsContent value={TabType.overview}>
              <Overview />
            </TabsContent>

            <TabsContent value={TabType.devices}>
              <Devices />
            </TabsContent>

            <TabsContent value={TabType.weather}>
              <Weather />
            </TabsContent>

            <TabsContent value={TabType.chart}>
              <Chart />
            </TabsContent>

            <TabsContent value={TabType.alert}>
              <AlertTab />
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </div>
  );
}
