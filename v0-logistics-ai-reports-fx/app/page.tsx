import Image from "next/image"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ThemeToggle } from "@/components/theme-toggle"
import { ReportsList } from "@/components/reports-list"

export default function ReportsListPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Image
                src="/cyberlogix-logo.jpeg"
                alt="CyberLogix.ai"
                width={280}
                height={50}
                className="h-12 w-auto"
                priority
              />
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <div className="flex flex-col items-end gap-1">
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <p className="text-sm font-semibold text-foreground">Janusz Trucker</p>
                    <p className="text-xs text-muted-foreground">Operations Manager</p>
                  </div>
                  <Avatar className="h-10 w-10">
                    <AvatarImage src="/professional-executive-manager-portrait.jpg" alt="Janusz Trucker" />
                    <AvatarFallback>JT</AvatarFallback>
                  </Avatar>
                </div>
                <p className="text-xs text-muted-foreground">Big Trucking Corp Ltd. • NIP: 314159265</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Now using real backend data */}
      <main className="container mx-auto px-6 py-8">
        <ReportsList />
      </main>
    </div>
  )
}
