"use client"

import { Label } from "@radix-ui/react-label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card"
import { TrendingUp } from "lucide-react"
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { AlertCircleIcon, CheckCircle2Icon, PopcornIcon } from "lucide-react"
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"


export default function AlertTab() {
  return (
    <div className="grid grid-cols-2 gap-5">
      <Card>
        <CardHeader>
          <CardTitle>Electric consumption too high</CardTitle>
          <CardDescription>January - June 2025</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid w-full max-w-xl items-start gap-4">
            <Alert>
              <CheckCircle2Icon />
              <AlertTitle>Success! Your changes have been saved</AlertTitle>
              <AlertDescription>
                This is an alert with icon, title and description.
              </AlertDescription>
            </Alert>
            <Alert>
              <PopcornIcon />
              <AlertTitle>
                This Alert has a title and an icon. No description.
              </AlertTitle>
            </Alert>
            <Alert variant="destructive">
              <AlertCircleIcon />
              <AlertTitle>Unable to process your payment.</AlertTitle>
              <AlertDescription>
                <p>Please verify your billing information and try again.</p>
                <ul className="list-inside list-disc text-sm">
                  <li>Check your card details</li>
                  <li>Ensure sufficient funds</li>
                  <li>Verify billing address</li>
                </ul>
              </AlertDescription>
            </Alert>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Electric consumption too high</CardTitle>
          <CardDescription>January - June 2025</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid w-full max-w-xl items-start gap-4">
            <Alert>
              <CheckCircle2Icon />
              <AlertTitle>Success! Your changes have been saved</AlertTitle>
              <AlertDescription>
                This is an alert with icon, title and description.
              </AlertDescription>
            </Alert>
            <Alert>
              <PopcornIcon />
              <AlertTitle>
                This Alert has a title and an icon. No description.
              </AlertTitle>
            </Alert>
            <Alert variant="destructive">
              <AlertCircleIcon />
              <AlertTitle>Unable to process your payment.</AlertTitle>
              <AlertDescription>
                <p>Please verify your billing information and try again.</p>
                <ul className="list-inside list-disc text-sm">
                  <li>Check your card details</li>
                  <li>Ensure sufficient funds</li>
                  <li>Verify billing address</li>
                </ul>
              </AlertDescription>
            </Alert>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}