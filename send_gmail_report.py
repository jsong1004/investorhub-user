# This script sends a post-event report to attendees using Gmail SMTP.
# Note: Gmail has a sending limit of 500 emails per day for free accounts.
# If you need to send more emails, consider using a different email service.
import os
import ssl
import csv
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for Gmail
USER_PORTAL_BASE_URL = os.getenv("USER_PORTAL_BASE_URL", "https://investorhub-user.ai-biz.app/user_portal")

def load_people_from_csv(file_path):
    """Loads a list of (name, email) tuples from the specified CSV file."""
    people = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header row
            for row in reader:
                if row and len(row) > 3: # Check if row has enough columns
                    name = row[0].strip()
                    email = row[3].strip()
                    if name and email and '@' in email: # Ensure both name and email are present and valid
                        people.append((name, email))
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return people

# PEOPLE list is now populated from the CSV file
PEOPLE = load_people_from_csv('data/Startup-World-Cup-Seattle-Regional-Guests.csv')

def send_report_email(name, email):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Startup World Cup Seattle Regional - Event Report</title>
    <style>
        /* Email-safe CSS */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
        }
        
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
        }
        
        .header {
            background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
            color: #ffffff;
            padding: 30px 20px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: bold;
        }
        
        .header p {
            margin: 0;
            font-size: 16px;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px 20px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #333333;
            font-size: 24px;
            margin: 0 0 15px 0;
            border-bottom: 3px solid #6B73FF;
            padding-bottom: 5px;
        }
        
        .section h3 {
            color: #6B73FF;
            font-size: 18px;
            margin: 20px 0 10px 0;
        }
        
        .highlight-box {
            background-color: #f8f9fa;
            border-left: 4px solid #6B73FF;
            padding: 20px;
            margin: 20px 0;
        }
        
        .stats-row {
            display: table;
            width: 100%;
            margin: 20px 0;
        }
        
        .stat-item {
            display: table-cell;
            text-align: center;
            padding: 15px 10px;
            background-color: #6B73FF;
            color: #ffffff;
            border-radius: 8px;
            margin: 0 5px;
            width: 23%;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 12px;
            margin-top: 5px;
            display: block;
        }
        
        .winners-section {
            background-color: #fff8dc;
            border: 2px solid #ffd700;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .winner-card {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .winner-card h4 {
            color: #333333;
            margin: 0 0 10px 0;
            font-size: 18px;
        }
        
        .score-badge {
            background-color: #ffd700;
            color: #333333;
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .keynote-box {
            background-color: #e8f4fd;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .keynote-box h4 {
            color: #1e88e5;
            margin: 0 0 15px 0;
        }
        
        .keynote-list {
            margin: 0;
            padding-left: 20px;
        }
        
        .keynote-list li {
            margin-bottom: 8px;
        }
        
        .thanks-section {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .sponsor-grid {
            display: table;
            width: 100%;
            margin: 15px 0;
        }
        
        .sponsor-column {
            display: table-cell;
            vertical-align: top;
            width: 33%;
            padding: 0 10px;
        }
        
        .sponsor-list {
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }
        
        .sponsor-list li {
            background-color: #ffffff;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #6B73FF;
            font-size: 14px;
        }
        
        .cta-button {
            display: inline-block;
            background-color: #ffd700;
            color: #333333;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            margin: 10px 5px;
            text-align: center;
        }
        
        .footer {
            background-color: #333333;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            font-size: 14px;
        }
        
        .footer a {
            color: #ffd700;
            text-decoration: none;
        }
        
        /* Mobile responsiveness for email */
        @media only screen and (max-width: 600px) {
            .stats-row {
                display: block;
            }
            
            .stat-item {
                display: block;
                width: 100%;
                margin: 5px 0;
            }
            
            .sponsor-grid {
                display: block;
            }
            
            .sponsor-column {
                display: block;
                width: 100%;
                padding: 0;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .content {
                padding: 20px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>🚀 Startup World Cup Seattle Regional</h1>
            <p>Event Report & Competition Results</p>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <!-- Event Summary -->
            <div class="section">
                <h2>🌟 Event Highlights</h2>
                <p>Thank you for being part of the Startup World Cup Seattle Regional! Our event brought together the brightest entrepreneurs, investors, and industry leaders in an exciting competition for a chance to represent Seattle at the global Startup World Cup finals and compete for a $1 million investment prize.</p>
                <p>This year's event even drew attention from the international startup community. Startups from South Korea and Argentina applied to pitch, including Cromodata, a company building a Marketplace for Tokenized Health Data, which flew in all the way from Argentina to compete for 1st place.</p>
                
                <div class="stats-row">
                    <div class="stat-item">
                        <span class="stat-number">300+</span>
                        <span class="stat-label">Registrants</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">150</span>
                        <span class="stat-label">Attendees</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">12</span>
                        <span class="stat-label">Companies</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">10</span>
                        <span class="stat-label">Judges</span>
                    </div>
                </div>
            </div>
            
            <!-- Keynote Insights -->
            <div class="section">
                <h2>🎤 Keynote Insights</h2>
                <div class="keynote-box">
                    <h4>Ron Wiener, CEO of Venture Mechanics: "What I've Learned from 40+ Years of Launching Startups"</h4>
                    <ul class="keynote-list">
                        <li><strong>Market Reality:</strong> Prepare for cataclysmic market collapses every 5-10 years</li>
                        <li><strong>Harsh Stats:</strong> Only 0.66% of startups that pitch VCs receive investment</li>
                        <li><strong>Quality Focus:</strong> When capital markets are down, only exceptional companies get funded</li>
                        <li><strong>2025 Outlook:</strong> May be one of the worst years for startup failures</li>
                        <li><strong>Exit Strategy:</strong> 99% of exits are acquisitions, not IPOs - plan accordingly</li>
                        <li><strong>Alternative Funding:</strong> Explore angels, revenue loans, and crowdfunding</li>
                        <li><strong>Accelerator Value:</strong> Quality improvement significantly improves your odds</li>
                    </ul>
                </div>
            </div>
            
            <!-- Winners Section -->
            <div class="section">
                <h2>🏆 Competition Winners</h2>
                <div class="winners-section">
                    <div class="winner-card">
                        <h4>🥇 1st Place: NewGem</h4>
                        <p><strong>FoodTech - Wraps Made from Fruits & Vegetables</strong></p>
                        <p>• 253 retail doors including Whole Foods, Safeway, Raley's<br>
                        • $1M revenue forecast for 2025<br>
                        • 64% gross margins with 20+ years team experience<br>
                        • Mondelez participation rights secured</p>
                    </div>
                    
                    <div class="winner-card">
                        <h4>🥈 2nd Place: Airbuild</h4>
                        <p><strong>Climate Tech - Carbon Capture & Water Treatment</strong></p>
                        <p>• $15.3M pipeline contracts in place<br>
                        • $1.68T total addressable market<br>
                        • PhD-level technical expertise<br>
                        • Unique combo technology for climate solutions</p>
                    </div>
                    
                    <div class="winner-card">
                        <h4>🥉 3rd Place: RealEngineers</h4>
                        <p><strong>HR Tech - AI-Powered Engineering Recruitment</strong></p>
                        <p>• Solving 250 candidates per job problem<br>
                        • $212B staffing market opportunity<br>
                        • 150+ customer discovery interviews completed<br>
                        • 6 years defense engineering background</p>
                    </div>
                </div>
            </div>
            
            <!-- Judge Insights -->
            <div class="section">
                <h2>🎯 Judge's Scoring Insights</h2>
                <div class="highlight-box">
                    <p>The judge's scoring heavily weighted <strong>current traction and revenue potential</strong>, with NewGem's proven retail presence and immediate revenue generation providing a significant advantage over earlier-stage companies.</p>
                    <p style="margin-top: 15px;">The competition showcased strong diversity across sectors - from sustainable food technology to climate solutions to HR tech - reflecting Seattle's innovative startup ecosystem.</p>
                </div>
            </div>
            
            <!-- Special Thanks -->
            <div class="section">
                <h2>🙏 Special Thanks</h2>
                <div class="thanks-section">
                    <h3>Distinguished Judges</h3>
                    <p>Angie Parker (Alliance of Angels), Valerie Trask (Tofinio), Jean-Philippe Persico (Shucker VC), Gabe Regalado (Graphene Ventures), Jesse Posey (Dreamward Ventures), Ron Wiener (Venture Mechanics), Levi Reed (Startup425), Mark Kotzer (Kotzer Consulting), Brian Frost (K-Startup Center), Ian Hameroff (Fulcrum Group)</p>
                    
                    <h3>Event Volunteers</h3>
                    <p>LeAnn Le (MC), Kyle Yoo (FD), Fred Hwang (Audience Support), Andrew Madson (Photographer), Eunsil Ha (Registration), UW Korean Student Association (Facility & Registration)</p>
                    
                    <h3>Sponsors & Partners</h3>
                    <div class="sponsor-grid">
                        <div class="sponsor-column">
                            <h4 style="color: #6B73FF; margin: 10px 0;">Media</h4>
                            <ul class="sponsor-list">
                                <li>GeekWire</li>
                                <li>INVEST: Startup & IPO News</li>
                            </ul>
                        </div>
                        <div class="sponsor-column">
                            <h4 style="color: #6B73FF; margin: 10px 0;">Accelerators</h4>
                            <ul class="sponsor-list">
                                <li>Venture Mechanics</li>
                                <li>Startup425</li>
                                <li>K-Startup Center</li>
                                <li>Tofinio</li>
                                <li>Matchstick Lab</li>
                                <li>Fulcrum Group</li>
                            </ul>
                        </div>
                        <div class="sponsor-column">
                            <h4 style="color: #6B73FF; margin: 10px 0;">Investors</h4>
                            <ul class="sponsor-list">
                                <li>Alliance of Angels</li>
                                <li>Shucker VC</li>
                                <li>Graphene Ventures</li>
                                <li>Dreamward Ventures</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- About Seattle Partners LLC -->
            <div class="section">
                <h2>🏢 About Seattle Partners LLC</h2>
                <div class="highlight-box">
                    <p>Seattle Partners LLC is a dynamic organization dedicated to fostering innovation and entrepreneurship in the Pacific Northwest region. As the organizing force behind events like the Startup World Cup Seattle Regional, Seattle Partners connects entrepreneurs, investors, and industry leaders to create meaningful opportunities for growth and collaboration.</p>

                    <h3 style="color: #ffd700; margin: 20px 0 10px 0;">Our Mission</h3>
                    <p>To build a thriving startup ecosystem in Seattle by facilitating connections between entrepreneurs and the resources they need to succeed, from early-stage funding to strategic partnerships and market opportunities.</p>

                    <h3 style="color: #ffd700; margin: 20px 0 10px 0;">What We Do</h3>
                    <ul style="margin: 15px 0;">
                        <li>Organize world-class startup competitions and pitch events</li>
                        <li>Connect entrepreneurs with investors and mentors</li>
                        <li>Facilitate strategic partnerships between startups and established companies</li>
                        <li>Promote Seattle as a global hub for innovation and technology</li>
                        <li>Support the growth of the Pacific Northwest startup ecosystem</li>
                    </ul>

                    <h3 style="color: #ffd700; margin: 20px 0 10px 0;">Coming Soon:</h3>
                    <p>Seattle Partners will evolve into Seattle Ventures with the launch of a new venture fund, aiming to make a greater impact on the PNW startup community. Seattle Ventures will focus on pre-seed and seed investments, offer equity-based acceleration programs, and run mission-based acceleration initiatives such as three-month revenue or growth guarantee programs. Additionally, the firm will provide cross-border acceleration services, helping bridge global startups with the U.S. market.</p>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://seattlepartners.us/" class="cta-button" target="_blank" style="background-color: #ffd700; color: #232b39; font-size: 18px; padding: 14px 32px; border-radius: 30px; font-weight: bold; display: inline-block; text-decoration: none;">
                            🌐 Visit Seattle Partners Website
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Thank you for being part of the Seattle startup ecosystem!</p>
            <p>For more information, visit <a href="https://seattlepartners.us/">seattlepartners.us</a></p>
            <p style="margin-top: 15px; font-size: 12px; opacity: 0.8;">Together, we're building the future of innovation in the Pacific Northwest.</p>
        </div>
    </div>
</body>
</html>
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Startup World Cup Seattle Regional - Event Report"
    msg.attach(MIMEText(html_content, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Sent report to {email}")
    except Exception as e:
        print(f"Failed to send to {email}: {e}")

def main():
    batch_size = 50
    total_people = len(PEOPLE)
    
    if total_people == 0:
        print("No people found in the CSV to email.")
        return

    print(f"Found {total_people} people to email. The script will pause after each batch of {batch_size}.")
    
    for i in range(0, total_people, batch_size):
        batch = PEOPLE[i:i + batch_size]
        batch_number = (i // batch_size) + 1
        total_batches = (total_people + batch_size - 1) // batch_size

        print(f"\n--- Sending batch {batch_number} of {total_batches} ({len(batch)} emails) ---")
        
        for name, email in batch:
            send_report_email(name, email) # Commented out for debugging
        
        print(f"--- Batch {batch_number} sent successfully. ---")

        if i + batch_size < total_people:
            try:
                input("Press Enter to send the next batch, or Ctrl+C to exit...")
            except KeyboardInterrupt:
                print("\nScript stopped by user.")
                break
    
    print("\nAll email batches have been processed.")

if __name__ == "__main__":
    main() 
